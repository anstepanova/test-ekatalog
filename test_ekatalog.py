import pytest
import re
import allure
import selenium

from allure_commons.types import AttachmentType
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


def make_screenshot(driver, filename=None):
    allure.attach(driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)


class LoginLogout:
    @staticmethod
    def login(driver, login, password):
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#mui_user_login_row > span'))
        )
        elem.click()
        make_screenshot(driver)
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-with-wrap clearfix"]/div[3]'))
        )
        elem.click()
        make_screenshot(driver)
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-name ek-form-group"]/input'))
        )
        elem.clear()
        elem.send_keys(login)
        make_screenshot(driver)
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="signin-password ek-form-group"]/input'))
        )
        elem.clear()
        elem.send_keys(password)
        make_screenshot(driver)
        elem = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@class="ek-form-btn blue"]'))
        )
        elem.click()
        make_screenshot(driver)
        return driver

    @staticmethod
    def logout(driver):
        elem = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span > a')
        elem.click()
        make_screenshot(driver, 'click_logout_button')
        return driver


class TestLogin:
    @allure.feature('Test login')
    @allure.story('Сhecking whether login was successful')
    @pytest.mark.parametrize('login, password', [
        (LOGIN, PASSWORD)
    ])
    def test_login(self, driver, login, password):
        with allure.step('Entering the username and password'):
            driver = LoginLogout.login(driver, login, password)
            elem = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, '#mui_user_login_row > a'))
            )
        with allure.step('Checking whether we logged into account'):
            make_screenshot(driver, 'click_logout_button')
            assert elem.text == 'Anastasia', make_screenshot(driver)
        with allure.step('Exiting from the account'):
            driver = LoginLogout.logout(driver)
            elem = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span')
            assert 'войти' in elem.text.lower(), make_screenshot(driver)


class TestCameras:
    @allure.feature('Test cameras')
    @allure.story('Сhecking existence the certain camera with a given brand among cameras with NFC')
    @pytest.mark.parametrize('brand, model', [
        ('Sony', 'HDR-AZ1VB')
    ])
    @pytest.mark.parametrize('login, password', [
        (LOGIN, PASSWORD)
    ])
    def test_find_cameras_with_nfc(self, driver, brand, model, login, password):
        with allure.step('Entering the username and password'):
            driver = LoginLogout.login(driver, login, password)
            user = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, '#mui_user_login_row > a'))
            )
            make_screenshot(driver)
            assert user.text == 'Anastasia', make_screenshot(driver)
        with allure.step('Click on gadgets in the main menu'):
            driver.find_element(By.CSS_SELECTOR,
                                'body > div.mainmenu.ff-roboto > div '
                                '> ul > li:nth-child(1) > a').click()
            make_screenshot(driver)
        with allure.step('Click on action cameras in the main menu'):
            driver.find_element(By.CSS_SELECTOR,
                                'body > div.mainmenu.ff-roboto > div > ul > li:nth-child(1) > div '
                                '> div > a.mainmenu-subitem.mainmenu-icon695 > img').click()
            make_screenshot(driver)
        with allure.step('Opening all brands of cameras '):
            all_brand = driver.find_element(By.CSS_SELECTOR, '#br_all > em')
            driver.execute_script("arguments[0].scrollIntoView(true);", all_brand)
            all_brand.click()
            make_screenshot(driver)
        with allure.step('Choosing the brand of the camera'):
            for i in range(1, 100):
                try:
                    current_brand = driver.find_element(By.XPATH, f'//*[@id="manufacturers_presets"]/ul/li[{i}]')
                    driver.execute_script("arguments[0].scrollIntoView(true);", current_brand)
                except Exception:
                    continue
                if current_brand.text.lower() == brand.lower():
                    current_brand.click()
                    break
                if i == 99:
                    assert False, make_screenshot(driver)
            make_screenshot(driver)
        with allure.step('Choosing NFC'):
            nfc = driver.find_element(By.CSS_SELECTOR, '#preset18920 > li:nth-child(8) > label')
            driver.execute_script("arguments[0].scrollIntoView(true);", nfc)
            nfc.click()
            make_screenshot(driver)
        with allure.step('Click on the button to show chosen cameras'):
            show = driver.find_element(By.CSS_SELECTOR, '#match_submit')
            driver.execute_script("arguments[0].scrollIntoView(true);", show)
            show.click()
            make_screenshot(driver)
        with allure.step('Finding the camera from testcase in the results of search and click on the camera'):
            needful_camera = f'{brand.lower()} {model.lower()}'
            camera = None
            cameras = driver.find_elements(By.XPATH, f'//*[@id="list_form1"]/div[*]'
                                                     f'/div[2]/table/tbody/tr/td[2]'
                                                     f'/table/tbody/tr/td[1]/a')
            for current_camera in cameras:
                if current_camera.text.lower() == needful_camera:
                    camera = current_camera
                    break
            if camera is None:
                assert False, make_screenshot(driver)
            camera.click()
            make_screenshot(driver)
        with allure.step('Adding the camera to bookmarks'):
            add_to_bookmarks = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, '#menu_addto > div:nth-child(1) > span'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", add_to_bookmarks)
            add_to_bookmarks.click()
            make_screenshot(driver)
        with allure.step('Opening the user\'s page. '
                         'Finding the camera in the bookmarks and removing one from there'):
            driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > a').click()
            make_screenshot(driver)
            bookmark = None
            bookmarks = driver.find_elements(By.XPATH, f'//*[@class="touchcarousel-container"]'
                                                       f'/div[*]/a[2]')
            for current_bookmark in bookmarks:
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
                    make_screenshot(driver)
                    break
            if bookmark is None:
                assert False, make_screenshot(driver)
        with allure.step('Opening the user\'s page. '
                         'Finding the camera in viewed ones and remove the camera from there'):
            driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > a').click()
            driver.find_element(By.XPATH, '//*[@class="user-menu__section wu_isaw"]').click()
            has_camera = False
            cameras = driver.find_elements(By.XPATH, f'//*[@class="user-history-div"]/a[*]')
            for i, current_camera in enumerate(cameras):
                camera_name_with_price = current_camera.text.lower()
                camera_name = camera_name_with_price[:camera_name_with_price.find('от')]
                camera_name = camera_name.strip()
                if camera_name == needful_camera:
                    has_camera = True
                    WebDriverWait(driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.XPATH, f'//*[@class="user-history-div"]/a[{i+1}]/div/div')
                        )
                    ).click()
                    make_screenshot(driver)
            if not has_camera:
                assert False, make_screenshot(driver)
        with allure.step('Exiting from the account'):
            LoginLogout.logout(driver)
            login = driver.find_element(By.CSS_SELECTOR, '#mui_user_login_row > span')
            assert 'войти' in login.text.lower(), make_screenshot(driver)


class TestTablets:
    @allure.feature('Test tablets')
    @allure.story('Choosing the tablets with max price, '
                  'price of any tablets must be under or equal the established value')
    @pytest.mark.parametrize('price', [
        1000,
        3000,
        6000,
        7000,
        8000,
        9000,
    ])
    def test_choosing_tablets_lower_than_set_price(self, price, driver):
        def get_tablets():
            tablets_with_range_of_price = driver.find_elements(By.XPATH, '//*[@class="model-price-range"]')
            tablets_with_one_price = driver.find_elements(By.XPATH, '//*[@class="pr31 ib"]')
            return tablets_with_range_of_price + tablets_with_one_price

        def get_price_from_str(s):
            price_from_str = re.search(r'\d+', s.replace(' ', ''))
            return int(price_from_str[0]) if price_from_str is not None else None

        with allure.step('Click on computers in the main menu'):
            driver.find_element(By.XPATH, '//*[@class="mainmenu-list ff-roboto"]/li[2]').click()
            make_screenshot(driver)
        with allure.step('Click on tablets in the main menu'):
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@class="mainmenu-subitem mainmenu-icon30"]')
                )
            ).click()
            make_screenshot(driver)
        with allure.step('Setting the max possible price'):
            max_price = driver.find_element(By.ID, 'maxPrice_')
            driver.execute_script("arguments[0].scrollIntoView(true);", max_price)
            max_price.clear()
            max_price.send_keys(price)
            make_screenshot(driver)
        with allure.step('Click on the button to show tablets with price under or equal established value'):
            show = driver.find_element(By.CSS_SELECTOR, '#match_submit')
            driver.execute_script("arguments[0].scrollIntoView(true);", show)
            show.click()
            make_screenshot(driver)
        with allure.step('Showing all tablets'):
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
            make_screenshot(driver)
        with allure.step('Getting all tablets and checking that the price are under or equal established value'):
            tablets = get_tablets()
            assert len(tablets) != 0, make_screenshot(driver)
            for tablet in tablets:
                tablet_price = get_price_from_str(tablet.text)
                assert tablet_price is not None and tablet_price < price, make_screenshot(driver)
