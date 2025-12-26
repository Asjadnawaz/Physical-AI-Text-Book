import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def explore_website_structure(base_url):
    """
    Systematically explore the website to find all accessible pages
    """
    print(f"Exploring website structure: {base_url}")

    # Get the main page
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the main page
    all_links = soup.find_all('a', href=True)
    print(f"Found {len(all_links)} links on the main page")

    # Categorize links
    internal_links = []
    doc_links = []

    for link in all_links:
        href = link['href']
        full_url = urljoin(base_url, href)

        # Check if it's an internal link
        if full_url.startswith(base_url):
            internal_links.append(full_url)

            # Check if it looks like a documentation page
            if '/docs/' in full_url or '/chapter' in full_url or '/intro' in full_url:
                doc_links.append(full_url)

    print(f"Found {len(internal_links)} internal links")
    print(f"Found {len(doc_links)} potential documentation links")

    # Check which links are actually accessible
    accessible_links = []
    for url in set(internal_links):  # Use set to remove duplicates
        try:
            # Remove fragment identifiers for checking
            clean_url = url.split('#')[0]
            response = requests.head(clean_url, timeout=10)
            if response.status_code == 200:
                accessible_links.append(url)
                print(f"[ACCESSIBLE] {url}")
            else:
                print(f"[NOT ACCESSIBLE - {response.status_code}] {url}")
        except Exception as e:
            print(f"[ERROR] {url} - {e}")

        time.sleep(0.1)  # Be respectful

    print(f"\nTotal accessible links: {len(accessible_links)}")

    # Get content from each accessible page to see what's available
    detailed_info = []
    for url in accessible_links:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                page_soup = BeautifulSoup(response.content, 'html.parser')

                # Get title and content length
                title = page_soup.title.string if page_soup.title else "No Title"
                content_length = len(response.text)

                detailed_info.append({
                    'url': url,
                    'title': title,
                    'content_length': content_length
                })

                print(f"  - {title[:50]}... (Content: {content_length} chars)")
        except Exception as e:
            print(f"  - Error getting details for {url}: {e}")

        time.sleep(0.1)  # Be respectful

    return detailed_info

if __name__ == "__main__":
    base_url = "https://physical-ai-text-book-lovat.vercel.app/"
    detailed_info = explore_website_structure(base_url)

    print(f"\nSummary: Found {len(detailed_info)} accessible pages")
    for info in detailed_info:
        print(f"  - {info['title'][:60]}... | {info['content_length']} chars | {info['url']}")