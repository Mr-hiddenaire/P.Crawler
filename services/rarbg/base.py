from config import coordinate
import time
import re
from utils.selenium.chrome import browser
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import pytesseract

def break_defence(url=None, is_success_landing_page='normal'):
    screenshot_filename = 'screenshot.png'
    captcha_filename = 'captcha.png'

    driver = browser.get_driver()
    driver.get(url)

    try:
        time.sleep(6)
        driver.find_element_by_link_text('Click here').click()
        driver.save_screenshot(screenshot_filename)
        make_screenshot_to_captcha_image(screenshot_filename=screenshot_filename, captcha_filename=captcha_filename)
        captcha_number = solve_captcha_number_from_image(filename=captcha_filename)

        driver.find_element_by_id('solve_string').send_keys(captcha_number)
        driver.find_element_by_id('button_submit').click()
        break_success = parse_break_defence_success(html=driver.page_source, is_success_landing_page=is_success_landing_page)

        if break_success is True:
            return driver
        else:
            driver.close()
            return None
    except NoSuchElementException:
        try:
            time.sleep(6)
            driver.save_screenshot(screenshot_filename)
            make_screenshot_to_captcha_image(screenshot_filename=screenshot_filename, captcha_filename=captcha_filename)
            captcha_number = solve_captcha_number_from_image(filename=captcha_filename)

            driver.find_element_by_id('solve_string').send_keys(captcha_number)
            driver.find_element_by_id('button_submit').click()
            break_success = parse_break_defence_success(html=driver.page_source, is_success_landing_page=is_success_landing_page)

            if break_success is True:
                return driver
            else:
                driver.close()
                return None
        except NoSuchElementException:
            return None

    return None

def make_screenshot_to_captcha_image(screenshot_filename=None, captcha_filename=None):
    im = Image.open(screenshot_filename)

    im2 = im.crop((coordinate.X, coordinate.Y, coordinate.X + coordinate.W, coordinate.Y + coordinate.H))
    im2.save(captcha_filename)

def solve_captcha_number_from_image(filename=None):
    img = Image.open(filename)
    number = pytesseract.image_to_string(img)

    return number

def parse_break_defence_success(html=None, is_success_landing_page='normal'):
    pattern = re.compile('mcpslar')
    result = re.findall(pattern, html)

    if is_success_landing_page == 'download':
        return True

    if len(result) > 0:
        return True
    else:
        return False