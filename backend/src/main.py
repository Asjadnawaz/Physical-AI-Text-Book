import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingPipeline:
    def __init__(self):
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.book_site_url = os.getenv("BOOK_SITE_URL", "https://physical-ai-text-book-lovat.vercel.app/")

    def get_all_urls(self, base_url: str) -> List[str]:
        """
        Get all URLs from the deployed book site
        """
        logger.info(f"Starting URL discovery from: {base_url}")
        urls = set()

        # First, try to get URLs from sitemap if available
        sitemap_url = urljoin(base_url, "sitemap.xml")
        try:
            sitemap_response = requests.get(sitemap_url)
            if sitemap_response.status_code == 200:
                logger.info("Found sitemap, extracting URLs...")
                # Parse XML using built-in ElementTree instead of BeautifulSoup for XML
                root = ET.fromstring(sitemap_response.content)
                sitemap_urls = []
                for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                    loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc_elem is not None:
                        url = loc_elem.text.strip()
                        if url.startswith(base_url):
                            sitemap_urls.append(url)

                # Check which sitemap URLs are accessible
                for url in sitemap_urls:
                    try:
                        response = requests.head(url, timeout=10)
                        if response.status_code == 200:
                            urls.add(url)
                        else:
                            logger.debug(f"Sitemap URL not accessible (Status {response.status_code}): {url}")
                    except Exception as e:
                        logger.debug(f"Sitemap URL error: {url} - {e}")
            else:
                logger.info("No sitemap.xml found or accessible")
        except Exception as e:
            logger.warning(f"Could not fetch sitemap: {e}")

        # If no URLs found from sitemap, try crawling the main site more thoroughly
        if not urls:
            logger.info("No URLs from sitemap, starting web crawling...")
            urls = self._crawl_site(base_url)

        # Also add the base URL itself if it's not already included
        try:
            response = requests.head(base_url, timeout=10)
            if response.status_code == 200:
                urls.add(base_url)
        except:
            pass

        # Also try to include sitemap.xml as it might contain additional content
        try:
            response = requests.head(sitemap_url, timeout=10)
            if response.status_code == 200:
                urls.add(sitemap_url)
        except:
            pass

        # Filter out URLs that return 404 or other errors (final validation)
        valid_urls = set()
        for url in urls:
            try:
                # Skip anchor links for initial validation
                clean_url = url.split('#')[0]
                response = requests.head(clean_url, timeout=10)
                if response.status_code == 200:
                    valid_urls.add(url)  # Add original URL (with anchor if present)
                else:
                    logger.debug(f"Final validation: Skipping URL with status {response.status_code}: {url}")
            except Exception as e:
                logger.debug(f"Final validation: Skipping URL due to error: {url} - {e}")

        logger.info(f"Found {len(valid_urls)} valid URLs to process")
        return list(valid_urls)

    def _crawl_site(self, base_url: str) -> set:
        """
        Simple crawler to find all URLs on the site
        """
        urls = set()
        visited = set()
        to_visit = [base_url]

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in visited or not current_url.startswith(self.book_site_url):
                continue

            visited.add(current_url)
            urls.add(current_url)

            try:
                # Respect robots.txt and rate limiting
                time.sleep(1)

                response = requests.get(current_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all links on the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)

                        # Only add URLs from the same domain
                        if urlparse(full_url).netloc == urlparse(base_url).netloc:
                            if full_url not in visited and full_url.startswith(self.book_site_url):
                                to_visit.append(full_url)

            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")
                continue

        return urls

    def extract_text_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extract clean text from a URL
        """
        logger.info(f"Extracting text from: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try to get main content - prioritize Docusaurus content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='container')

            if main_content:
                # Remove navigation and sidebar elements
                for nav in main_content.find_all(['nav', 'aside']):
                    nav.decompose()

                text = main_content.get_text()
            else:
                # Fallback to body content
                body = soup.find('body')
                if body:
                    # Remove common non-content elements
                    for elem in body.find_all(['nav', 'aside', 'header', 'footer', 'script', 'style']):
                        elem.decompose()
                    text = body.get_text()
                else:
                    text = soup.get_text()

            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "text": text
            }

        except Exception as e:
            logger.error(f"Error extracting text from {url}: {e}")
            return {
                "url": url,
                "title": "",
                "text": ""
            }

    def chunk_text(self, text: str, chunk_size: int = 512) -> List[str]:
        """
        Split text into chunks of specified size (in tokens approximately)
        """
        if not text:
            return []

        # Simple approach: split by sentences and group into chunks
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
            else:
                current_chunk += sentence + ". "

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        if not texts:
            return []

        logger.info(f"Generating embeddings for {len(texts)} text chunks")

        try:
            response = self.cohere_client.embed(
                texts=texts,
                model="embed-multilingual-v3.0",  # Using multilingual model for technical content
                input_type="search_document"  # Specify the input type for Cohere
            )

            embeddings = [embedding for embedding in response.embeddings]
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return [[] for _ in texts]  # Return empty embeddings in case of error

    def create_collection(self, collection_name: str = "rag_embedding"):
        """
        Create Qdrant collection for storing embeddings
        """
        logger.info(f"Creating Qdrant collection: {collection_name}")

        try:
            # Check if collection already exists
            collections = self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if collection_name in collection_names:
                logger.info(f"Collection {collection_name} already exists, recreating...")
                self.qdrant_client.delete_collection(collection_name)

            # Create new collection with 1024 dimensions (default for Cohere embeddings)
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )

            logger.info(f"Successfully created collection: {collection_name}")
            return True

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False

    def save_chunk_to_qdrant(self, chunk_text: str, embedding: List[float], metadata: Dict[str, Any],
                           collection_name: str = "rag_embedding"):
        """
        Save a text chunk with its embedding to Qdrant
        """
        try:
            # Generate a unique ID for this record
            import hashlib
            text_hash = hashlib.md5(chunk_text.encode()).hexdigest()

            # Upsert the record to Qdrant
            self.qdrant_client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=text_hash,
                        vector=embedding,
                        payload={
                            "text": chunk_text,
                            "source_url": metadata.get("source_url", ""),
                            "chunk_index": metadata.get("chunk_index", 0),
                            "title": metadata.get("title", ""),
                            "created_at": time.time()
                        }
                    )
                ]
            )

            return True

        except Exception as e:
            logger.error(f"Error saving chunk to Qdrant: {e}")
            return False

    def execute_pipeline(self):
        """
        Execute the complete embedding pipeline
        """
        logger.info("Starting embedding pipeline execution...")

        # Step 1: Get all URLs
        urls = self.get_all_urls(self.book_site_url)
        if not urls:
            logger.error("No URLs found, stopping pipeline")
            return

        # Step 2: Create Qdrant collection
        if not self.create_collection("rag_embedding"):
            logger.error("Failed to create Qdrant collection, stopping pipeline")
            return

        # Step 3: Process each URL
        total_chunks = 0
        for i, url in enumerate(urls):
            logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

            # Extract text from URL
            content = self.extract_text_from_url(url)
            if not content["text"]:
                logger.warning(f"No text extracted from {url}, skipping")
                continue

            # Chunk the text
            chunks = self.chunk_text(content["text"])

            # Generate embeddings for chunks
            if chunks:
                embeddings = self.embed(chunks)

                # Save each chunk with its embedding to Qdrant
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    if embedding:  # Only save if embedding was generated successfully
                        metadata = {
                            "source_url": url,
                            "chunk_index": idx,
                            "title": content["title"]
                        }

                        success = self.save_chunk_to_qdrant(
                            chunk_text=chunk,
                            embedding=embedding,
                            metadata=metadata
                        )

                        if success:
                            total_chunks += 1
                        else:
                            logger.error(f"Failed to save chunk {idx} from {url}")

        logger.info(f"Pipeline completed! Processed and saved {total_chunks} text chunks to Qdrant.")


def main():
    """
    Main function to execute the embedding pipeline
    """
    pipeline = EmbeddingPipeline()
    pipeline.execute_pipeline()


if __name__ == "__main__":
    main()