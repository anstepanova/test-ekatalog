import pytest

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


@pytest.fixture
def driver():
    driver = selenium.webdriver.Chrome('./chromedriver')
    driver.get('https://www.e-katalog.ru/')
    yield driver
    driver.quit()


def make_screenshot(driver, filename):
    driver.save_screenshot(f'results/{filename}.png')


class TestMainPage:
    def test_main_page_loading(self, driver):
        driver.get('https://www.e-katalog.ru/')
        assert 'e-katalog' in driver.title.lower()


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


class TestLoginLogout:
    @pytest.mark.parametrize('login, password', [
        ('***', '***')
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




