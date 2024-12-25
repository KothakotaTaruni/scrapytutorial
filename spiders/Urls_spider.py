import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class WebCrawler:
    def __init__(self, seed_urls, allowed_domains, disallowed_urls, max_depth):
        self.seed_urls = seed_urls
        self.allowed_domains = allowed_domains
        self.disallowed_urls = disallowed_urls
        self.max_depth = max_depth
        self.crawled_urls = set()

    def crawl(self):
        for seed_url in self.seed_urls:
            self._crawl(seed_url, 0)

    def _crawl(self, url, depth):
        if depth > self.max_depth:
            return

        if url in self.crawled_urls:
            return

        self.crawled_urls.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find product pages
        product_pages = self._find_product_pages(soup, url)

        for product_page in product_pages:
            # Extract product information
            product_info = self._extract_product_info(product_page)

            # Store or process product information
            print(product_info)

        # Crawl linked pages
        linked_pages = self._find_linked_pages(soup, url)
        for linked_page in linked_pages:
            self._crawl(linked_page, depth + 1)

    def _find_product_pages(self, soup, url):
        # Implement logic to find product pages
        # For example, look for pages with a specific class or attribute
        product_pages = []
        for link in soup.find_all('a', class_='product-link'):
            product_pages.append(urljoin(url, link.get('href')))
        return product_pages
