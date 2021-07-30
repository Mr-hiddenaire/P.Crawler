from models.contents_model import Contents
from config import base as base_config

class ContentService:
    def __init__(self):
        pass

    def add_contents(self, data=None):
        for info in data:
            obj = self.get_content_by_detail_url_hash(info['detail_url_hash'], info['types'])
            if hasattr(obj, 'id') is False:
                Contents.add_contents(Contents(info['name'], info['unique_id'], info['tags'], info['types'], info['thumb_url'], info['torrent_url'], info['detail_url'], info['pick_up_status'], info['pick_up_time'], info['is_archive'], info['archive_priority'], info['list_url_hash'], info['detail_url_hash']))

    @staticmethod
    def is_page_scraped(url_hash=None, types=None):
        total_scraped = Contents.is_page_scraped(url_hash, types)

        if types == base_config.IS_ASIA:
            if total_scraped >= base_config.ASIA_SCRAPED_FLAG:
                return True
            else:
                return False
        if types == base_config.IS_EURO:
            if total_scraped >= base_config.EURO_SCRAPED_FLAG:
                return True
            else:
                return False

    @staticmethod
    def get_content_by_detail_url_hash(url_hash=None, types=None):
        info = Contents.get_content_by_detail_url_hash(url_hash, types)
        return info