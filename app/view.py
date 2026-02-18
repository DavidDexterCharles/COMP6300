from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def render_users(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request},
    )


def render_users2(request: Request):
    """
    Teaching note:
    This page demonstrates login (JWT), and authenticated CRUD for per-user items (notes).
    """

    return templates.TemplateResponse(
        "user2.html",
        {"request": request},
    )