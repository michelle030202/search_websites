from urllib.parse import urlparse


'''
http://news.walla.co.il/news => co.il
'''
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return str(results[-2]) + "." + str(results[-1])

    except:
        return ''

'''
http://news.walla.co.il/news => news.walla.co.il
'''
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


