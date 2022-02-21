from urllib.request import urlopen
from link_finder import LinksFinder
from general import *
from bs4 import BeautifulSoup
from urllib import request
from crawler_db import CrawlerDb

# to solve SSL: CERTIFICATE_VERIFY_FAILED
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Crawler:
    # class variable (shared among all instance)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    crawlerdb = CrawlerDb()

    def __init__(self, project_name, base_url, domain_name):
        Crawler.project_name = project_name
        Crawler.base_url = base_url  # base_url = walla.co.il, page_url = walla.co.il/1000
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.project_name + '/urls_to_crawl.txt'
        Crawler.crawled_file = Crawler.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page(Crawler.base_url)

    @staticmethod
    def boot():
        create_project_dir(Crawler.project_name)
        create_data_files(Crawler.project_name, Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    '''
    The function gets url, and check if its already crawled.
    If its not crawled yet, crawl the url:
    1. gets page title.
    2. add links of url to queue, that start with base url.
    3. removes the url from queue.
    4. update files with updated queue.
    5. add to db page url + title.
    '''
    @staticmethod
    def crawl_page(page_url):
        if page_url not in Crawler.crawled:
            print('now crawling ' + page_url)
            print(' Queue ' + str(len(Crawler.queue)) + ' | crawled ' + str(len(Crawler.crawled)))
            page_title = Crawler.get_title(page_url)
            Crawler.add_links_to_queue(Crawler.gather_links(page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files()
            print("Page url: " + page_url)
            print("page title: " + page_title)
            Crawler.crawlerdb.add_link_and_title(str(page_url), str(page_title))

    '''
    Get page title.
    '''
    @staticmethod
    def get_title(page_url):
        html = request.urlopen(page_url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        print("title: ", title.string)
        return title.string

    @staticmethod
    def gather_links(page_url):
        try:
            response = urlopen(page_url)
            html_bytes = response.read()
            # base_url = walla.co.il, page_url = walla.co.il/1000
            finder = LinksFinder(Crawler.base_url, page_url)
            page_links = finder.get_all_links_that_start_with_base_url()
            print(page_links)
        except:
            print('Error: can not crawl page')
            return set()
        return page_links

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Crawler.queue:
                continue
            if url in Crawler.crawled:
                continue
            if Crawler.domain_name not in url:
                continue
            Crawler.queue.add(url)
            print("added url: ", url)

    @staticmethod
    def update_files():
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)