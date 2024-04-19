from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqladmin import Admin
from . import models, schemas, utils
from .database import engine, get_db
from admin import views, auth as admin_auth
from .routers import article, user, auth, pages


# orm
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = 'Spider-verse'
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


@app.get('/')
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("login.html", {"request": request})

