import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def discover_valid_urls(base_url):
    """
    Discover valid URLs from the textbook website
    """
    print(f"Discovering valid URLs from: {base_url}")

    # Get the main page to find navigation links
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for navigation links in common Docusaurus navigation elements
    nav_links = set()

    # Look for sidebar links
    sidebar_links = soup.find_all('a', href=True)
    for link in sidebar_links:
        href = link['href']
        full_url = urljoin(base_url, href)

        # Only include internal links that look like documentation pages
        if (full_url.startswith(base_url) and
            ('/docs/' in full_url or full_url.endswith('/') or '#' not in href)):
            nav_links.add(full_url)

    # Filter for actual accessible pages
    valid_urls = set()
    for url in nav_links:
        try:
            # Skip anchor links
            if '#' in url and url.split('#')[0] != base_url:
                url = url.split('#')[0]

            # Check if the page exists
            page_response = requests.get(url)
            if page_response.status_code == 200:
                valid_urls.add(url)
                print(f"[VALID] Valid URL found: {url}")
            else:
                print(f"[INVALID] Invalid URL (Status {page_response.status_code}): {url}")

            # Be respectful with requests
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Error checking URL {url}: {e}")

    return list(valid_urls)

if __name__ == "__main__":
    base_url = "https://physical-ai-text-book-lovat.vercel.app/"
    valid_urls = discover_valid_urls(base_url)
    print(f"\nFound {len(valid_urls)} valid URLs:")
    for url in valid_urls:
        print(f"  - {url}")