from config import searcher as config_searcher
from config import base as base_config
from pyquery import PyQuery
import json
import requests
from utils.selenium.chrome import browser
import logging
from urllib.parse import urlparse
import re

def find_torrent(unique_id=None):
    g_cse_api = config_searcher.GOOGLE_API_URL % (unique_id, config_searcher.GOOGLE_CSE_CX, config_searcher.GOOGLE_CSE_API_KEY, base_config.GOOGLE_CSE_QUERY_NUM)
    print(g_cse_api)
    exit()
    response = requests.get(g_cse_api, headers={'User-Agent': base_config.USER_AGENT})

    logging.info('G-CES.result: ' + response.text)

    json_result = json.loads(response.text)

    """ G CSE retrieve fail """
    if 'items' not in json_result:
        return None

    g_cse_items = json_result['items']

    for g_cse_item in g_cse_items:
        if g_cse_item['displayLink'] in config_searcher.SEARCH_TARGET_DOMAINS:

            func_name = config_searcher.SEARCH_TARGET_DOMAINS[g_cse_item['displayLink']]
            func_name = 'parse_' + func_name

            print(g_cse_item['link'] + '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

            torrent_url = eval(func_name)(url=g_cse_item['link'], unique_id=unique_id)
            if torrent_url is not None:
                return torrent_url
            else:
                continue

    return None

def parse_1337x(url=None, unique_id=None):
    """
    response = requests.get(url, headers={'User-Agent': base.USER_AGENT})
    doc = PyQuery(response.text)

    """

    """ driver initialization """
    driver = browser.get_driver()

    driver.get(url)

    doc = PyQuery(driver.page_source)

    download_url_html = doc('.dropdown-menu li').eq(0)

    download_url_doc = doc(download_url_html)

    torrent_url = download_url_doc('a').attr('href')

    if torrent_url is not None:
        torrent_url = torrent_url.replace('http', 'https')
        torrent_is_valid = is_valid_torrent_judged_via_http_status(torrent_url=torrent_url)

        if torrent_is_valid is True:
            driver.close()
            return torrent_url
        else:
            """ Parse out the torrent, but it maybe invalid """
            driver.close()
            return None
    else:
        driver.close()
        """ Stop to further request temporarily """
        #torrent_url = parse_1337x_extra(url=url, unique_id=unique_id)
        return torrent_url

def parse_1337x_extra(url=None, unique_id=None):

    """ driver initialization """
    driver = browser.get_driver()

    driver.get(url)
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    new_url = domain + '/search/' + unique_id + '/1/'

    driver.get(new_url)

    doc = PyQuery(driver.page_source)

    """ Only check once """
    for html in doc('tbody tr').items():
        doc = PyQuery(html)
        page_url = doc('td a').eq(1).attr('href')
        title = doc('td a').eq(1).text()

        pattern = re.compile(unique_id)
        result = re.findall(pattern, title)

        if len(result) > 0:
            driver.get(domain + page_url)

            doc = PyQuery(driver.page_source)

            download_url_html = doc('.dropdown-menu li').eq(0)

            download_url_doc = doc(download_url_html)

            torrent_url = download_url_doc('a').attr('href')

            torrent_url = torrent_url.replace('http', 'https')

            driver.close()
            return torrent_url
        else:
            return None

    return None

def parse_limetorrents(url=None):
    """
    response = requests.get(url, headers={'User-Agent': base.USER_AGENT})

    doc = PyQuery(response.text)

    """

    """ driver initialization """
    driver = browser.get_driver()

    driver.get(url)

    doc = PyQuery(driver.page_source)

    torrent_url = doc('.downloadarea').eq(0).find('a').attr('href')

    if torrent_url is not None:
        torrent_url = torrent_url.replace('http', 'https')
        torrent_is_valid = is_valid_torrent_judged_via_http_status(torrent_url=torrent_url)

        if torrent_is_valid is True:
            driver.close()
            return torrent_url
        else:
            """ Parse out the torrent, but it maybe invalid """
            driver.close()
            return None
    else:
        driver.close()
        return None

""" To judge whether torrent is valid or not via response history """
def is_valid_torrent_judged_via_http_status(torrent_url=None):
    response = requests.get(torrent_url, headers={'User-Agent': base_config.USER_AGENT})

    """ There is history,it indicates invalid """
    if len(response.history) <= 0:
        return True
    else:
        return False