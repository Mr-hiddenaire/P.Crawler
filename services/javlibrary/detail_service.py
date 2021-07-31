import logging
import time
from utils.selenium.chrome import browser
from pyquery import PyQuery

def do_original_source_crawler_with_selenium(detail_url=None):
    logging.info('detail url:' + detail_url + ' >>>>>> is scraping')

    """ driver initialization """
    driver = browser.get_driver()
    driver.get(detail_url)

    """ sleep 6 sec to wait for cf protection finish """
    time.sleep(6)

    html = driver.page_source
    driver.close()

    return html

def get_html_generator_according_to_original_html(original_html=None):
    doc = PyQuery(original_html)

    html_generator = doc('.genre').items()

    return html_generator

def parse_data_according_to_html_generator(html_generator=None):
    result = []
    for html in html_generator:
        doc_tag = PyQuery(html)
        tag = doc_tag('a').text()

        result.append(tag)

    result = {
        'tags': ','.join(result)
    }

    return result