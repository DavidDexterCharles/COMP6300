from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError

import model

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str
    email: EmailStr

@router.get("/")
def users_page():
    return {"message": "Hello world"}


@router.get("/api/users")
def api_list_users(db: Session = Depends(model.get_db)):
    users = db.query(model.User).order_by(model.User.id.desc()).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


@router.get("/api/users/{user_id}")
def api_get_user(user_id: int, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/api/users", status_code=status.HTTP_201_CREATED)
def api_create_user(payload: UserCreate, db: Session = Depends(model.get_db)):
    user = model.User(name=payload.name, email=payload.email)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    return {"id": user.id, "name": user.name, "email": user.email}


@router.put("/api/users/{user_id}")
def api_update_user(user_id: int, payload: UserUpdate, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.name = payload.name
    user.email = payload.email

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    return {"id": user.id, "name": user.name, "email": user.email}


@router.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_id: int, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
