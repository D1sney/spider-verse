from sqladmin import ModelView
from app import models


class UserAdmin(ModelView, model=models.User):
    # столбцы которые будут показываться в общем списке
    column_list = [models.User.id, models.User.username]
    # столбцы которые будут показываться в детализированной странице
    column_details_exclude_list = [models.User.password]
    
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    category = "accounts"


class ArticleAdmin(ModelView, model=models.Article):
    # показать все столбцы которые есть в модели
    column_list = "__all__"
    name = "Article"
    name_plural = "Articles"
    icon = "fa-solid fa-newspaper"
    category = "main_page"