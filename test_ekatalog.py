import pytest
import re

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from resources.testing_data import *


@pytest.fixture
def driver():
    driver = selenium.webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('https://www.e-katalog.ru/')
    yield driver
    driver.quit()


def make_screenshot(driver, filename):
    driver.save_screenshot(f'results/{filename}.png')


class LoginLogout:
    @staticmethod
    def login(driver, login, password):
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#mui_user_login_row > span'))
        )
        elem.click()
        make_screenshot(driver, 'click_login_button')
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-with-wrap clearfix"]/div[3]'))
        )
        elem.click()
        make_screenshot(driver, 'click_login_email_button')
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-name ek-form-group"]/input'))
        )
        elem.clear()
        elem.send_keys(login)
        make_screenshot(driver, 'enter_login_input_login_button')
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-password ek-form-group"]/input'))
        )
        elem.clear()
        elem.send_keys(password)
        make_screenshot(driver, 'enter_login_input_password_button')
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="ek-form-btn blue"]'))
        )
        elem.click()
        make_screenshot(driver, 'click_login_send_username_password_button')
        return driver

    @staticmethod
    def logout(driver):
        elem = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span > a')
        elem.click()
        make_screenshot(driver, 'click_logout_button')
        return driver


class TestLogin:
    @pytest.mark.parametrize('login, password', [
        (LOGIN, PASSWORD)
    ])
    def test_login(self, driver, login, password):
        driver = LoginLogout.login(driver, login, password)
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '#mui_user_login_row > a'))
        )
        assert elem.text == 'Anastasia'
        driver = LoginLogout.logout(driver)
        elem = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span')
        assert 'войти' in elem.text.lower()


class TestCameras:
    @pytest.mark.parametrize('brand, model', [
        ('Sony', 'HDR-AZ1VB')
    ])
    @pytest.mark.parametrize('login, password', [
        (LOGIN, PASSWORD)
    ])
    def test_find_cameras_with_nfc(self, driver, brand, model, login, password):
        driver = LoginLogout.login(driver, login, password)
        user = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '#mui_user_login_row > a'))
        )
        assert user.text == 'Anastasia'
        driver.find_element(By.CSS_SELECTOR,
                            'body > div.mainmenu.ff-roboto > div '
                            '> ul > li:nth-child(1) > a').click()
        make_screenshot(driver, 'click_gadget_button')
        driver.find_element(By.CSS_SELECTOR,
                            'body > div.mainmenu.ff-roboto > div > ul > li:nth-child(1) > div '
                            '> div > a.mainmenu-subitem.mainmenu-icon695 > img').click()
        make_screenshot(driver, 'click_action_cameras_button')
        all_brand = driver.find_element(By.CSS_SELECTOR, '#br_all > em')
        driver.execute_script("arguments[0].scrollIntoView(true);", all_brand)
        all_brand.click()
        make_screenshot(driver, 'click_all_brand_button')
        for i in range(1, 100):
            try:
                current_brand = driver.find_element(By.XPATH, f'//*[@id="manufacturers_presets"]/ul/li[{i}]')
                driver.execute_script("arguments[0].scrollIntoView(true);", current_brand)
            except Exception:
                continue
            if current_brand.text.lower() == brand.lower():
                current_brand.click()
                make_screenshot(driver, 'choice_brand')
                break
            if i == 99:
                assert False
        nfc = driver.find_element(By.CSS_SELECTOR, '#preset18920 > li:nth-child(8) > label')
        driver.execute_script("arguments[0].scrollIntoView(true);", nfc)
        nfc.click()
        make_screenshot(driver, 'choice_nfc')
        show = driver.find_element(By.CSS_SELECTOR, '#match_submit')
        driver.execute_script("arguments[0].scrollIntoView(true);", show)
        show.click()
        make_screenshot(driver, 'click_show_button')
        needful_camera = f'{brand.lower()} {model.lower()}'
        camera = None
        for i in range(1, 100):
            try:
                current_camera = driver.find_element(By.XPATH, f'//*[@id="list_form1"]/div[{i}]'
                                                               f'/div[2]/table/tbody/tr/td[2]'
                                                               f'/table/tbody/tr/td[1]/a/span')
                driver.execute_script("arguments[0].scrollIntoView(true);", current_camera)
            except Exception:
                continue
            if current_camera.text.lower() == needful_camera:
                camera = current_camera
                driver.execute_script("window.scrollBy(0, -100)", camera)
                camera = driver.find_element(By.XPATH, f'//*[@id="list_form1"]/div[{i}]'
                                                       f'/div[2]/table/tbody/tr/td[2]'
                                                       f'/table/tbody/tr/td[1]/a')
                break
        if camera is None:
            assert False
        camera.click()
        make_screenshot(driver, 'click_on_camera')
        add_to_bookmarks = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '#menu_addto > div:nth-child(1) > span'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_to_bookmarks)
        add_to_bookmarks.click()
        make_screenshot(driver, 'add_camera_to_bookmarks')
        driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > a').click()
        make_screenshot(driver, 'open_bookmarks')
        bookmark = None
        for i in range(1, 100):
            try:
                current_bookmark = driver.find_element(By.XPATH, f'//*[@class="touchcarousel-container"]'
                                                                 f'/div[{i}]/a[2]/span')
            except Exception:
                continue
            if current_bookmark.text.lower() == needful_camera:
                bookmark = current_bookmark
                current_bookmark.click()
                remove_bookmark = driver.find_element(By.CSS_SELECTOR, '#menu_addto > div:nth-child(1) > span')
                driver.execute_script('arguments[0].scrollIntoView(true);', remove_bookmark)
                remove_bookmark.click()
                remove_bookmark = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, '//*[@class="wishlist-item-name"]')
                    )
                )
                driver.execute_script('arguments[0].scrollIntoView(true);', remove_bookmark)
                remove_bookmark.click()
                make_screenshot(driver, 'remove_camera_from_bookmarks')
                break
        if bookmark is None:
            assert False
        driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > a').click()
        driver.find_element(By.XPATH, '//*[@class="user-menu__section wu_isaw"]').click()
        has_camera = False
        for i in range(1, 100):
            try:
                current_camera = driver.find_element(By.XPATH, f'//*[@class="user-history-div"]/a[{i}]/u')
            except Exception:
                continue
            if current_camera.text.lower() == needful_camera:
                has_camera = True
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, f'//*[@class="user-history-div"]/a[{i}]/div/div')
                    )
                ).click()
        if not has_camera:
            assert False
        LoginLogout.logout(driver)
        login = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span')
        assert 'войти' in login.text.lower()


class TestTablets:
    @pytest.mark.parametrize('price', [
        1000,
        3000,
        6000,
    ])
    def test_choosing_tablets_lower_than_set_price(self, price, driver):
        def get_tablets():
            tablets_with_range_of_price = driver.find_elements(By.XPATH, '//*[@class="model-price-range"]')
            tablets_with_one_price = driver.find_elements(By.XPATH, '//*[@class="pr31 ib"]')
            return tablets_with_range_of_price + tablets_with_one_price

        def get_price_from_str(s):
            price_from_str = re.search(r'\d+', s.replace(' ', ''))
            return int(price_from_str[0]) if price_from_str is not None else None

        driver.find_element(By.XPATH, '//*[@class="mainmenu-list ff-roboto"]/li[2]').click()
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="mainmenu-subitem mainmenu-icon30"]')
            )
        ).click()
        max_price = driver.find_element(By.ID, 'maxPrice_')
        driver.execute_script("arguments[0].scrollIntoView(true);", max_price)
        max_price.clear()
        max_price.send_keys(price)
        show = driver.find_element(By.CSS_SELECTOR, '#match_submit')
        driver.execute_script("arguments[0].scrollIntoView(true);", show)
        show.click()
        can_show_more = True
        while can_show_more:
            try:
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, '//*[@class="list-more-div h blue-button"]')
                    )
                ).click()
            except Exception as e:
                can_show_more = False
        tablets = get_tablets()
        assert len(tablets) != 0
        for tablet in tablets:
            tablet_price = get_price_from_str(tablet.text)
            assert tablet_price is not None and tablet_price < price







