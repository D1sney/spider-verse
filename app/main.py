from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, utils
from .database import engine, get_db
from admin import views, auth as admin_auth
from .routers import article, user, auth, pages, like
from .config import settings


# orm
# теперь когда у нас в проекте есть alembic у нас нет необходимости в этой строчке которая создает таблицы по sqlalchemy моделям, если таблиц с такими названиями не существует
# при запуске CI в github actions эта строчка будет вызывать ошибку, так как через workflow файл мы будем создавать только бд для тестирования, а так как обычной бд не будет, будет ошибка, потому что в этой строчке engine обращается к обычной бд
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = 'Spider-verse'
)

# важно не добавлять слеш в конце url чтобы все работало корректно
origins = [settings.BASE_URL, utils.add_www(settings.BASE_URL)]
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# важно назвать не templates и не statics, чтобы не было конфликтов имен с sqladmin
template = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Админка
admin = Admin(app, engine, authentication_backend=admin_auth.authentication_backend)
admin.add_view(views.UserAdmin)
admin.add_view(views.ArticleAdmin)


# Подключение роутеров
app.include_router(article.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(like.router)


@app.get('/')
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("login.html", {"request": request, "base_url": settings.BASE_URL})

