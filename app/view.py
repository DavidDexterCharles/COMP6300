from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def render_users(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request},
    )