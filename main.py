from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    driver.get('https://www.e-katalog.ru/')
    driver.close()


if __name__ == '__main__':
    main()