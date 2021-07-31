from config import base as base_config
import logging
import time
from services.rarbg import base as rarbg_base_service
from pyquery import PyQuery
import re

def do_original_source_crawler_with_selenium(detail_url=None):
    logging.info('detail url:' + detail_url + ' >>>>>> is scraping')

    """ driver initialization """
    driver = rarbg_base_service.break_defence(url=detail_url)
    if driver is not None:
        driver.get(detail_url)

        """ sleep 6 sec to wait for cf protection finish """
        time.sleep(6)

        html = driver.page_source
        driver.close()
        return html
    else:
        logging.info('Web driver initialization of break defence fail')

def parse_data_according_to_original_html(original_html=None):
    tag = []

    doc = PyQuery(original_html)

    torrent_url = doc('table[class="lista"]').find('tr').eq(0).find('td').eq(1).find('a').attr('href')

    pattern = re.compile('Tags:<\/td>(.*?)<\/tr>')
    tag_html = re.findall(pattern, original_html)

    if len(tag_html) > 0:
        tag_doc = PyQuery(tag_html[0])
        for tag_a_html in tag_doc('td').find('a').items():
            tag_a_doc = PyQuery(tag_a_html)
            tag.append(tag_a_doc('a').text())

    result = {
        'torrent_url': base_config.CRAWLER_URL_EURO + torrent_url,
        'tags': ','.join(tag),
    }

    return result