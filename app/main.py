from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqladmin import Admin
from . import models, schemas, utils
from .database import engine, get_db
from admin import views
from .routers import article, user


# orm
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = 'Spider-verse'
)

# важно назвать не templates и не statics, чтобы не было конфликтов имен с sqladmin
template = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Админка
admin = Admin(app, engine)
admin.add_view(views.UserAdmin)
admin.add_view(views.ArticleAdmin)


# Подключение роутеров
app.include_router(article.router)
app.include_router(user.router)


@app.get('/')
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("index.html", {"request": request})

