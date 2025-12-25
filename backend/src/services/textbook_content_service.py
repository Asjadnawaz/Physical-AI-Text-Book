import os
import uuid
from datetime import datetime
from typing import List
from pathlib import Path
from ..models.textbook_content import TextbookContent
from ..services.retrieval_service import RetrievalService
from ..config.settings import settings


class TextbookContentService:
    """
    Service for processing and managing textbook content
    """

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.content_path = Path(settings.TEXTBOOK_CONTENT_PATH)

    def process_textbook_content(self):
        """
        Process all textbook markdown files and store them in the vector database
        """
        # Find all markdown files in the textbook content directory
        markdown_files = list(self.content_path.rglob("*.md"))

        for file_path in markdown_files:
            self._process_markdown_file(file_path)

    def _process_markdown_file(self, file_path: Path):
        """
        Process a single markdown file and store its content in the vector database
        """
        try:
            # Read the content of the markdown file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract the relative path for the page_path
            relative_path = file_path.relative_to(self.content_path)
            page_path = f"/{relative_path.with_suffix('').as_posix()}"

            # Get the section title from the first heading in the file
            section_title = self._extract_title(content)

            # Split the content into chunks
            chunks = self._split_content(content, max_chunk_size=1000)

            # Process each chunk
            for i, chunk_content in enumerate(chunks):
                content_id = str(uuid.uuid4())

                textbook_content = TextbookContent(
                    id=content_id,
                    page_path=page_path,
                    section_title=f"{section_title} - Part {i+1}" if len(chunks) > 1 else section_title,
                    content=chunk_content,
                    chunk_index=i,
                    created_at=datetime.now()
                )

                # Store the content in the vector database
                self.retrieval_service.store_textbook_content(
                    content_id=textbook_content.id,
                    content=textbook_content.content,
                    page_path=textbook_content.page_path,
                    section_title=textbook_content.section_title
                )

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

    def _extract_title(self, content: str) -> str:
        """
        Extract the title from markdown content (first heading)
        """
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                # Remove the # and any leading/trailing whitespace
                title = line.strip('# ')
                return title
        return "Untitled Section"

    def _split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split content into chunks of approximately max_chunk_size characters
        """
        if len(content) <= max_chunk_size:
            return [content]

        chunks = []
        paragraphs = content.split('\n\n')

        current_chunk = ""
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # If any chunk is still too large, split by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= max_chunk_size:
                final_chunks.append(chunk)
            else:
                # Split large chunk by sentences
                sentences = chunk.split('. ')
                current_sentence_chunk = ""
                for sentence in sentences:
                    sentence_with_period = sentence + '. '
                    if len(current_sentence_chunk + sentence_with_period) <= max_chunk_size:
                        current_sentence_chunk += sentence_with_period
                    else:
                        if current_sentence_chunk:
                            final_chunks.append(current_sentence_chunk.strip())
                        current_sentence_chunk = sentence_with_period

                if current_sentence_chunk.strip():
                    final_chunks.append(current_sentence_chunk.strip())

        return final_chunks

    def get_content_for_page(self, page_path: str) -> List[TextbookContent]:
        """
        Get all content chunks for a specific textbook page
        """
        # This would typically query the database for content by page_path
        # For now, we'll return an empty list as this is primarily a retrieval function
        # The actual content would be retrieved via the retrieval service
        return []