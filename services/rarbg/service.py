from config import base as base_config
import logging
from pyquery import PyQuery
from utils.tool import hash_with_blake2b
from services.content import ContentService
from services.rarbg import base as rarbg_base_service

def do_original_source_crawler_with_selenium(url=None):
    url_hash = hash_with_blake2b(url)
    is_scraped = ContentService.is_page_scraped_v2()

    if is_scraped is False:
        logging.info('url:' + url + ' >>>>>> hash:' + url_hash + ' is scraping')

        """ driver initialization """
        driver = rarbg_base_service.break_defence(url=url)

        if driver is not None:
            driver.get(url)
            html = driver.page_source
            driver.close()

            return html
        else:
            logging.info('Web driver initialization of break defence fail')
    else:
        logging.info('url:' + url + ' >>>>>> hash:' + url_hash + ' is scraped')

def get_html_generator_according_to_original_html(original_html=None):
    doc = PyQuery(original_html)

    html_generator = doc('.lista2').items()

    return html_generator

def parse_data_according_to_html_generator(html_generator=None, base_url=None):
    result = []
    for html in html_generator:
        doc = PyQuery(html)

        name = doc('tr').find('td').eq(1).find('a').text()
        unique_id = 'NaN'
        """ Value assignation later """
        tags = ''
        types = base_config.IS_EURO
        """ No need it anymore. thumbnail will be generated by ffmpeg """
        thumb_url = ''
        """ Value assignation later """
        torrent_url = ''
        """ Value assignation later """
        torrent_path = ''
        entry_point = base_url
        detail_url = base_config.CRAWLER_URL_EURO + doc('tr').find('td').eq(1).find('a').attr('href')
        pick_up_status = 0
        pick_up_time = 0
        is_archive = 0
        archive_priority = 0
        list_url_hash = hash_with_blake2b(base_url)
        detail_url_hash = hash_with_blake2b(detail_url)
        is_scraped = 0

        info = {
            'name': name,
            'unique_id': unique_id,
            'tags': tags,
            'types': types,
            'thumb_url': thumb_url,
            'torrent_url': torrent_url,
            'torrent_path': torrent_path,
            'entry_point': entry_point,
            'detail_url': detail_url,
            'pick_up_status': pick_up_status,
            'pick_up_time': pick_up_time,
            'is_archive': is_archive,
            'archive_priority': archive_priority,
            'list_url_hash': list_url_hash,
            'detail_url_hash': detail_url_hash,
            'is_scraped': is_scraped,
        }

        result.append(info)

    return result