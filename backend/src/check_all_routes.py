import requests
from urllib.parse import urljoin
import time

def check_common_routes(base_url):
    """
    Check common Docusaurus routes that might exist
    """
    print(f"Checking common routes for: {base_url}")

    # Common Docusaurus and documentation routes
    common_routes = [
        "/",  # Main page
        "/docs",  # Documentation root
        "/docs/intro",
        "/docs/getting-started",
        "/docs/about",
        "/docs/about-textbook",
        "/docs/chapter-1",
        "/docs/chapter-1/section-1",
        "/docs/chapter-2",
        "/docs/chapter-3",
        "/docs/chapter-4",
        "/docs/glossary",
        "/docs/references",
        "/docs/api",
        "/blog",
        "/blog/intro",
        "/sitemap.xml",
        "/sitemap-docs.xml",
        "/pages",
        "/categories",
        "/tags",
        "/exercises",
        "/tutorials",
        "/examples",
        "/api-docs",
        "/static",
        "/assets"
    ]

    accessible_routes = []
    for route in common_routes:
        full_url = urljoin(base_url, route)
        try:
            response = requests.head(full_url, timeout=10)
            if response.status_code == 200:
                # Get content details
                get_response = requests.get(full_url, timeout=10)
                content_length = len(get_response.text)
                title = "Unknown"

                # Try to extract title from HTML
                if '<title>' in get_response.text:
                    start = get_response.text.find('<title>') + 7
                    end = get_response.text.find('</title>', start)
                    if start > 6 and end > start:
                        title = get_response.text[start:end].strip()

                accessible_routes.append({
                    'url': full_url,
                    'status': response.status_code,
                    'content_length': content_length,
                    'title': title
                })

                print(f"[200] {full_url} | {content_length} chars | {title[:50]}...")
            elif response.status_code == 404:
                print(f"[404] {full_url}")
            else:
                print(f"[{response.status_code}] {full_url}")

        except Exception as e:
            print(f"[ERROR] {full_url} - {e}")

        time.sleep(0.1)  # Be respectful

    return accessible_routes

if __name__ == "__main__":
    base_url = "https://physical-ai-text-book-lovat.vercel.app/"
    accessible_routes = check_common_routes(base_url)

    print(f"\nSUMMARY: Found {len(accessible_routes)} accessible routes")
    for route in accessible_routes:
        print(f"  - {route['title'][:60]}... | {route['content_length']} chars | {route['url']}")