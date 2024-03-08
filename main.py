from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title = 'Spider-verse'
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Jinja почему-то не подключает к нашему html соседние css стили, а строчка выше подключает
# FileResponse и HTMLResponse тоже не подключают

# templates = Jinja2Templates(directory="static")

# @app.get("/", response_class=HTMLResponse)
# async def get_main_page(request: Request):
#     return templates.TemplateResponse(
#         request=request, context={'message': 'Hello'}, status_code=201
#     )