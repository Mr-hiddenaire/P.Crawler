import logging
from services.content import ContentService
from config import base as base_config
from services.javlibrary.torrentor import TorrentorService

def do_asia():
    page = 1
    offset = (page - 1)*base_config.COMMON_PAGES_SIZE
    page_size = 100

    list_result = ContentService.get_content_not_scraped_torrent_url_is_empty(offset=offset, page_size=page_size, types=base_config.IS_ASIA, is_scraped=base_config.DETAIL_SCRAPED_STATUS)
    for info in list_result:
        torrent_url = TorrentorService().find_torrent(info.unique_id)
        if torrent_url is not None:
            logging.info('The torrent url of ' + info.detail_url + ' is ' + torrent_url)
            ContentService.update_content_by_pk(pk=info.id, data={'torrent_url': torrent_url})
        else:
            logging.info(info.detail_url + ' >>> has no torrent url')

def main():
    do_asia()

if __name__ == '__main__':
    main()