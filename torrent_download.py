from config import base as base_config
from random import randint
from services.content import ContentService
from services.javlibrary.downloader import Downloader as JavlibraryDownloader
from services.rarbg.downloader import Downloader as RarbgDownloader
from utils import tool

def do_asia():
    page = 1
    total = ContentService.get_total_torrent_not_download(types=base_config.IS_ASIA, is_scraped=base_config.DETAIL_SCRAPED_STATUS)
    pages = (total / base_config.COMMON_PAGES_SIZE) + 1

    while page <= pages:
        offset = (page - 1) * base_config.COMMON_PAGES_SIZE
        list_result = ContentService.get_content_torrent_not_download(offset=offset, page_size=base_config.COMMON_PAGES_SIZE, types=base_config.IS_ASIA, is_scraped=base_config.DETAIL_SCRAPED_STATUS)
        for info in list_result:
            torrent_path = JavlibraryDownloader(torrent_url=info.torrent_url).download()
            if torrent_path is not None:
                ContentService.update_content_by_pk(pk=info.id, data={'torrent_path': torrent_path, 'is_scraped': base_config.TORRENT_SCRAPED_STATUS})
        page = page + 1

def do_euro():
    page = 1
    total = ContentService.get_total_torrent_not_download(types=base_config.IS_EURO, is_scraped=base_config.DETAIL_SCRAPED_STATUS)
    pages = (total / base_config.COMMON_PAGES_SIZE) + 1

    while page <= pages:
        offset = (page - 1) * base_config.COMMON_PAGES_SIZE
        list_result = ContentService.get_content_torrent_not_download(offset=offset, page_size=base_config.COMMON_PAGES_SIZE, types=base_config.IS_EURO, is_scraped=base_config.DETAIL_SCRAPED_STATUS)
        for info in list_result:
            torrent_path = RarbgDownloader(torrent_url=info.torrent_url).download()
            if torrent_path is not None:
                ContentService.update_content_by_pk(pk=info.id, data={'torrent_path': torrent_path, 'is_scraped': base_config.TORRENT_SCRAPED_STATUS})
        page = page + 1

def check_process_exists_or_not_specialty():
    tool.check_process_exists_or_not('ps -ef |grep -v grep |grep chrome')
    tool.check_process_exists_or_not('ps -ef |grep -v grep |grep google')

def main():
    check_process_exists_or_not_specialty()

    n = randint(base_config.IS_ASIA, base_config.IS_EURO)
    func = base_config.MAP_FUNC[n]
    eval(func)()

if __name__ == '__main__':
    main()