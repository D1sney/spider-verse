# Без юнит тестов

# from selenium import webdriver
# # test that main page opens
# browser = webdriver.Chrome()
# browser.get('http://127.0.0.1:8000')
# assert 'Spider-verse' in browser.title

# На юнит тестах
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    # когда начинаем работать
    def setUp(self):
        # отключение DevTools listening в терминале
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.browser = webdriver.Chrome(options=options)

    # когда работа выполнена
    def tearDown(self):  
        self.browser.quit()

    # проверяем Spider-verse в титуле страницы
    def test_home_page_title(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('Spider-verse', self.browser.title)
        # self.fail('Finish the test!')

    # проверяем заголовок страницы, Miles Morales должно быть
    def test_home_page_header(self):
        self.browser.get('http://127.0.0.1:8000')
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Miles Morales', header)


if __name__ == '__main__':
    unittest.main()