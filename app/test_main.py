# from fastapi.testclient import TestClient
# from main import app, Article

# client = TestClient(app)

# def test_get_main_page():
#     response = client.get("/")
#     html = response.content.decode('utf-8')
#     assert response.status_code == 200
#     assert html.startswith('<!DOCTYPE html>')
#     assert '<title>Spider-verse</title>' in response.text
#     assert '<h1>Miles Morales</h1>' in response.text
#     assert html.endswith('</html>')



# def test_article_model_save_and_retrieve(self):
#     # создай статью 1
#     # сохрани статью 1 в базе
#     article1 = Article(
#         title='article 1',
#         full_text='full_text 1',
#         summary='summary 1',
#         category='category 1',
#     )
#     article1.save()

#     # создай статью 2
#     # сохрани статью 2 в базе
#     article2 = Article(
#         title='article 2',
#         full_text='full_text 2',
#         summary='summary 2',
#         category='category 2',
#     )
#     article2.save()

#     # загрузи из базы все статьи
#     all_articles = Article.objects.all()

#     # проверь: статей должно быть 2
#     self.assertEqual(len(all_articles), 2)
#     # проверь: первая загруженная из базы статья == статья 1
#     self.assertEqual(
#         all_articles[0].title,
#         article1.title
#     )
#     # проверь: вторая загруженная из базы статья == статья 2
#     self.assertEqual(
#         all_articles[1].title,
#         article2.title
#     )