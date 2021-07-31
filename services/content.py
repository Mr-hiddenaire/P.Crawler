from models.contents_model import Contents
from config import base as base_config

class ContentService:
    def __init__(self):
        pass

    def add_contents(self, data=None):
        for info in data:
            obj = self.get_content_by_detail_url_hash(url_hash=info['detail_url_hash'], types=info['types'])
            if hasattr(obj, 'id') is False:
                Contents().add_contents(name=info['name'], unique_id=info['unique_id'], tags=info['tags'], types=info['types'], thumb_url=info['thumb_url'], torrent_url=info['torrent_url'], entry_point=info['entry_point'], detail_url=info['detail_url'], pick_up_status=info['pick_up_status'], pick_up_time=info['pick_up_time'], is_archive=info['is_archive'], archive_priority=info['archive_priority'], list_url_hash=info['list_url_hash'], detail_url_hash=info['detail_url_hash'], is_scraped=info['is_scraped'])
                inserted_info = Contents.get_content_by_detail_url_hash(url_hash=info['detail_url_hash'], types=info['types'])
                Contents.update_content_by_pk(pk=inserted_info.id, data={'is_scraped': base_config.LIST_SCRAPED_STATUS})

    @staticmethod
    def is_page_scraped(url_hash=None, types=None):
        total_scraped = Contents.is_page_scraped(url_hash=url_hash, types=types)

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
        info = Contents.get_content_by_detail_url_hash(url_hash=url_hash, types=types)
        return info

    @staticmethod
    def get_total_not_scraped_by_type(types=None, is_scraped=None):
        total = Contents.get_total_not_scraped_by_type(types=types, is_scraped=is_scraped)
        return total

    @staticmethod
    def get_contents_not_scraped_by_type(offset=None, page_size=None, types=None, is_scraped=None):
        list_result = Contents.get_contents_not_scraped_by_type(offset=offset, page_size=page_size, types=types, is_scraped=is_scraped)
        return list_result

    @staticmethod
    def update_content_by_pk(pk=None, data=None):
        res = Contents.update_content_by_pk(pk=pk, data=data)
        return res

    @staticmethod
    def get_content_not_scraped_torrent_url_is_empty(offset=None, page_size=None, types=None, is_scraped=None):
        list_result = Contents.get_content_not_scraped_torrent_url_is_empty(offset=offset, page_size=page_size, types=types, is_scraped=is_scraped)
        return list_result