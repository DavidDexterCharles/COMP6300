from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError

import model
import view

router = APIRouter()


@router.get("/users")
def users_page(request: Request):
    return view.render_users(request)


class UserCreate(BaseModel):
    name: str
    email: EmailStr


@router.get("/api/users")
def api_list_users(db: Session = Depends(model.get_db)):
    users = db.query(model.User).order_by(model.User.id.desc()).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@router.post("/api/users")
def api_create_user(payload: UserCreate, db: Session = Depends(model.get_db)):
    user = model.User(name=payload.name, email=payload.email)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return {"error": "Email already exists"}

    return {"id": user.id, "name": user.name, "email": user.email}
