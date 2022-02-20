from urllib.request import urlopen
from link_finder import LinkFinder
from general import *
from bs4 import BeautifulSoup
from urllib import request
from crawler_db import CrawlerDb

# to solve SSL: CERTIFICATE_VERIFY_FAILED
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Spider:
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
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_directory(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print(' Queue ' + str(len(Spider.queue)) + ' | crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            page_title = Spider.get_title(page_url)
            print("--------")
            print(page_url)
            print(page_title)
            Spider.crawlerdb.add_link_and_title(str(page_url), str(page_title))
            #add_to_db(page_url, page_title)


    @staticmethod
    def get_title(page_url):
        html = request.urlopen(page_url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        print("title: ", title.string)
        return title.string

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            #if response.getheader('Content-Type') == 'text/html':
            html_bytes = response.read()
            html_string = html_bytes.decode('utf-8')

            #base_url = walla.co.il, page_url = walla.co.il/1000
            finder = LinkFinder(Spider.base_url, page_url)
            page_links = finder.get_all_links_that_start_with_base_url()
            print(page_links)
            #finder.feed(html_string)
        except:
            print('Error: can not crawl page')
            return set()
        return page_links

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)
            print("added url: ", url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)