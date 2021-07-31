from config import searcher as searcher_config
from utils.selenium.chrome import browser
from pyquery import PyQuery

class TorrentorService:
    def __init__(self):
        self.torrent_main_entry = searcher_config.TORRENT_MAIN_URL + searcher_config.TORRENT_MAIN_URI

    def find_torrent(self, unique_id=None):
        self.torrent_main_entry = self.torrent_main_entry + unique_id
        original_html = self.do_original_source_crawler_with_selenium()
        html_generator = self.get_html_generator_according_to_original_html(original_html=original_html)
        torrent_url = self.parse_data_according_to_html_generator(html_generator=html_generator)
        return torrent_url

    def do_original_source_crawler_with_selenium(self):
        driver = browser.get_driver()
        driver.get(self.torrent_main_entry)
        original_html = driver.page_source
        return original_html

    @staticmethod
    def get_html_generator_according_to_original_html(original_html=None):
        doc = PyQuery(original_html)
        html_generator = doc('.table2 .tt-name').items()
        return html_generator

    @staticmethod
    def parse_data_according_to_html_generator(html_generator=None):
        result = []
        for html in html_generator:
            doc = PyQuery(html)
            torrent_url = doc.find('a').attr('href')
            result.append(torrent_url)
        if len(result)  > 0:
            return result[0]
        return None

