from selenium import webdriver


def main():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://www.e-katalog.ru/')
    driver.close()


if __name__ == '__main__':
    main()