from config import base as base_config
from random import randint
from services.content import ContentService
from services.javlibrary import detail_service as javlibrary_detail_service
from services.rarbg import detail_service as rarbg_detail_service
from utils import tool

def main():
    check_process_exists_or_not_specialty()

    n = randint(base_config.IS_ASIA, base_config.IS_EURO)
    func = base_config.MAP_FUNC[n]
    eval(func)()

def check_process_exists_or_not_specialty():
    tool.check_process_exists_or_not('ps -ef |grep -v grep |grep chrome')
    tool.check_process_exists_or_not('ps -ef |grep -v grep |grep google')

def do_asia():
    page = 1
    total = ContentService.get_total_not_scraped_by_type(types=base_config.IS_ASIA, is_scraped=base_config.LIST_SCRAPED_STATUS)
    pages = (total / base_config.COMMON_PAGES_SIZE) + 1

    while page <= pages:
        offset = (page - 1)*base_config.COMMON_PAGES_SIZE
        list_result = ContentService.get_contents_not_scraped_by_type(offset=offset, page_size=base_config.COMMON_PAGES_SIZE, types=base_config.IS_ASIA, is_scraped=base_config.LIST_SCRAPED_STATUS)
        for info in list_result:
            original_html = javlibrary_detail_service.do_original_source_crawler_with_selenium(detail_url=info.detail_url)
            if original_html is not None:
                html_generator = javlibrary_detail_service.get_html_generator_according_to_original_html(original_html=original_html)
                data = javlibrary_detail_service.parse_data_according_to_html_generator(html_generator=html_generator)
                ContentService.update_content_by_pk(pk=info.id, data={'tags': data['tags'], 'is_scraped': base_config.DETAIL_SCRAPED_STATUS})
        page = page + 1

def do_euro():
    page = 1
    total = ContentService.get_total_not_scraped_by_type(types=base_config.IS_EURO, is_scraped=base_config.LIST_SCRAPED_STATUS)
    pages = (total / base_config.COMMON_PAGES_SIZE) + 1

    while page <= pages:
        offset = (page - 1) * base_config.COMMON_PAGES_SIZE
        list_result = ContentService.get_contents_not_scraped_by_type(offset=offset, page_size=base_config.COMMON_PAGES_SIZE, types=base_config.IS_EURO, is_scraped=base_config.LIST_SCRAPED_STATUS)
        for info in list_result:
            original_html = rarbg_detail_service.do_original_source_crawler_with_selenium(detail_url=info.detail_url)
            if original_html is not None:
                data = rarbg_detail_service.parse_data_according_to_original_html(original_html=original_html)
                ContentService.update_content_by_pk(pk=info.id, data={'torrent_url': data['torrent_url'], 'tags': data['tags'], 'is_scraped': base_config.DETAIL_SCRAPED_STATUS})
        page = page + 1

if __name__ == '__main__':
    main()