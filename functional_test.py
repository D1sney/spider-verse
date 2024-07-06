# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By


# class NewVisitorTest(unittest.TestCase):
#     # когда начинаем работать
#     def setUp(self):
#         # отключение DevTools listening в терминале
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
#         self.browser = webdriver.Chrome(options=options)

#     # когда работа выполнена
#     def tearDown(self):  
#         self.browser.quit()

#     # проверяем Spider-verse в титуле страницы
#     def test_home_page_title(self):
#         self.browser.get('http://127.0.0.1:8000')
#         self.assertIn('Spider-verse', self.browser.title)
#         # self.fail('Finish the test!')

#     # проверяем заголовок страницы, Miles Morales должно быть
#     def test_home_page_header(self):
#         self.browser.get('http://127.0.0.1:8000')
#         header = self.browser.find_element(By.TAG_NAME, 'h1').text
#         self.assertIn('Miles Morales', header)

#     # под заголовком страницы должен быть новостной блок из статей
#     def test_home_page_news(self):
#         self.browser.get('http://127.0.0.1:8000')
#         article_list = self.browser.find_element(By.CLASS_NAME, 'article-list')
#         self.assertTrue(article_list)
        
#     # у каждой статьи должен быть заголовок и абзац с текстом
#     def test_home_page_articles_look_correct(self):
#         self.browser.get('http://127.0.0.1:8000')
#         article_title = self.browser.find_element(By.CLASS_NAME, 'article-title')
#         article_summary = self.browser.find_element(By.CLASS_NAME, 'article-summary')
#         self.assertTrue(article_title)
#         self.assertTrue(article_summary)

    


# if __name__ == '__main__':
#     unittest.main()