from bs4 import BeautifulSoup
import urllib.request

class LinkFinder:
    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url

    def get_all_links_that_start_with_base_url(self):
        page_links = []
        parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
        resp = urllib.request.urlopen(self.page_url)
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

        for link in soup.find_all('a', href=True):
            print(link['href'])
            if link['href'].startswith(self.base_url):
                if link['href'] not in page_links:
                    page_links.append(link['href'])
                    print("added link ", link['href'])
        return page_links