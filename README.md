# test-ekatalog
![](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue) ![](https://img.shields.io/badge/allure-2.13.8-blue)

Testing e-katalog.ru site using selenium. 
The tests  are placed in `test_ekatalog.py`. The allure report is placed in `allure_report` directory. The documentation is placed in `documentation.md`. 

## Setting up the environment 
To create virtual environment:
```python3 -m venv venv```

To activate the virtual environment:
``` source venv/bin/activate```

To install dependencies:
```python install -r requirements.txt```

## Running the tests
It's necessary to install `ChromeDriver` ![https://pypi.org/project/selenium/](https://pypi.org/project/selenium/)

To enable Allure listener to collect results during the test execution:
```pytest --alluredir=allure_report```

To run the test:
```py.test --alluredir=allure_report test_ekatalog.py```

To see the actual report after the tests have finished:
```allure serve allure_report```

