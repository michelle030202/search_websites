from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'News'
HOMEPAGE = 'https://news.walla.co.il/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
URLS_TO_CRAWL = PROJECT_NAME + '/urls_to_crawl.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def crawl():
    while True:
        links = file_to_set(URLS_TO_CRAWL)
        for url in links:
            Spider.crawl_page(url)

crawl()