import logging
from config import base as base_config
from random import randint
from services.javlibrary import service as javlibrary_service
from services.rarbg import service as rarbg_service
from services.content import ContentService

logging.basicConfig(filename='log.log',level=logging.INFO, format='%(levelname)s:%(asctime)s %(message)s')

def main():
    n = randint(base_config.IS_ASIA, base_config.IS_EURO)
    func = base_config.MAP_FUNC[n]
    eval(func)()

def do_asia():
    page = 1

    while page <= base_config.CRAWLER_MAX_PAGE:
        requested_url = base_config.CRAWLER_URL_ASIA + base_config.CRAWLER_URI_ASIA % page

        original_html = javlibrary_service.do_original_source_crawler_with_selenium(url=requested_url)
        if original_html is not None:
            html_generator = javlibrary_service.get_html_generator_according_to_original_html(original_html=original_html)
            data = javlibrary_service.parse_data_according_to_html_generator(html_generator=html_generator, base_url=requested_url)
            ContentService().add_contents(data=data)
        page = page + 1

def do_euro():
    page = 1

    while page <= base_config.CRAWLER_MAX_PAGE:
        requested_url = base_config.CRAWLER_URL_EURO + base_config.CRAWLER_URI_EURO % page

        original_html = rarbg_service.do_original_source_crawler_with_selenium(url=requested_url)
        if original_html is not None:
            html_generator = rarbg_service.get_html_generator_according_to_original_html(original_html=original_html)
            data = rarbg_service.parse_data_according_to_html_generator(html_generator=html_generator, base_url=requested_url)
            ContentService().add_contents(data=data)
        page = page + 1

if __name__ == '__main__':
    main()