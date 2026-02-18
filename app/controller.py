from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import base64
import hashlib
import hmac
import os
from typing import Optional
from datetime import datetime, timedelta, timezone

import jwt

import model
import view

router = APIRouter()


# ----------------------------
# JWT configuration (teaching)
# ----------------------------
# In production, you should store this in an environment variable.
# Many teams load environment variables from a `.env` file in production
# (for example with python-dotenv). We don't enforce that here.
# For teaching purposes we fall back to a default value.
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 60

bearer_scheme = HTTPBearer(auto_error=False)


def _hash_password(password: str) -> str:
    """
    Teaching note:
    - Never store raw passwords
    - Use a slow hash (PBKDF2) with a random salt
    - Store the parameters with the hash so we can verify later
    """

    if not password or len(password) < 4:
        # Minimal teaching guardrail (not strong policy)
        raise ValueError("Password must be at least 4 characters")

    iterations = 120_000
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

    salt_b64 = base64.urlsafe_b64encode(salt).decode("utf-8").rstrip("=")
    dk_b64 = base64.urlsafe_b64encode(dk).decode("utf-8").rstrip("=")
    return f"pbkdf2_sha256${iterations}${salt_b64}${dk_b64}"


def _verify_password(password: str, stored: str) -> bool:
    """
    Verify a password against our stored PBKDF2 format.
    We use `hmac.compare_digest` to avoid timing attacks.
    """

    try:
        scheme, iter_str, salt_b64, dk_b64 = stored.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False

        iterations = int(iter_str)
        # Add '=' padding back for base64 decoding
        salt = base64.urlsafe_b64decode(salt_b64 + "==")
        expected_dk = base64.urlsafe_b64decode(dk_b64 + "==")

        actual_dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(actual_dk, expected_dk)
    except Exception:
        return False


def _create_token(user: model.User) -> str:
    """
    Create a JWT for a user.
    Payload fields:
    - sub: subject (we store user id as a string)
    - email: convenience claim for teaching/debugging
    - exp: expiration timestamp (required for time-limited tokens)
    """

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": now + timedelta(minutes=JWT_EXPIRES_MINUTES),
        "iat": now,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(model.get_db),
) -> model.User:
    """
    Dependency that enforces authentication.

    Teaching note:
    Most real APIs expect the token in the header:
      Authorization: Bearer <token>

    For teaching / quick testing, we also allow a query parameter:
      ?token=<token>
    """

    # Prefer the Authorization header (standard).
    token = credentials.credentials if credentials else None

    # Teaching fallback: allow ?token=... so students can test in a browser easily.
    if not token:
        token = request.query_params.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token. Send Authorization: Bearer <token> or ?token=<token>",
        )

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


@router.get("/users")
def users_page(request: Request):
    return view.render_users(request)


@router.get("/users2")
def users2_page(request: Request):
    return view.render_users2(request)


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class RegisterPayload(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class NoteCreate(BaseModel):
    text: str


class NoteDelete(BaseModel):
    note_id: int


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


@router.get("/api/users/{user_id}")
def api_get_user(user_id: int, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        return {"error": "User not found"}
    return {"id": user.id, "name": user.name, "email": user.email}


@router.put("/api/users/{user_id}")
def api_update_user(user_id: int, payload: UserUpdate, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        return {"error": "User not found"}

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = str(payload.email)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return {"error": "Email already exists"}

    return {"id": user.id, "name": user.name, "email": user.email}


@router.delete("/api/users/{user_id}")
def api_delete_user(user_id: int, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        return {"error": "User not found"}

    # Teaching note: delete dependent data in the simplest way
    db.query(model.Note).filter(model.Note.user_id == user_id).delete()
    db.query(model.UserCredential).filter(model.UserCredential.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"ok": True}


# ----------------------------
# Auth endpoints (JWT)
# ----------------------------

@router.post("/api/register")
def api_register(payload: RegisterPayload, db: Session = Depends(model.get_db)):
    """
    Register creates:
    - a user row in `users`
    - a password hash row in `user_credentials`
    """

    try:
        password_hash = _hash_password(payload.password)
    except ValueError as e:
        return {"error": str(e)}

    user = model.User(name=payload.name, email=str(payload.email))
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return {"error": "Email already exists"}

    cred = model.UserCredential(user_id=user.id, password_hash=password_hash)
    db.add(cred)
    db.commit()

    token = _create_token(user)
    return {"token": token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email}}


@router.post("/api/login")
def api_login(payload: LoginPayload, db: Session = Depends(model.get_db)):
    user = db.query(model.User).filter(model.User.email == str(payload.email)).first()
    if user is None:
        return {"error": "Invalid email or password"}

    cred = db.query(model.UserCredential).filter(model.UserCredential.user_id == user.id).first()
    if cred is None:
        return {"error": "User has no password set (register again)"}

    if not _verify_password(payload.password, cred.password_hash):
        return {"error": "Invalid email or password"}

    token = _create_token(user)
    return {"token": token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email}}


@router.get("/api/me")
def api_me(current_user: model.User = Depends(get_current_user)):
    """
    AUTH REQUIRED.
    Use `Authorization: Bearer <token>` or `?token=<token>`.
    """
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}


# ----------------------------
# Authenticated notes endpoints
# ----------------------------

@router.get("/api/notes")
def api_list_notes(
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(model.get_db),
):
    """
    AUTH REQUIRED.
    Use `Authorization: Bearer <token>` or `?token=<token>`.
    """
    notes = (
        db.query(model.Note)
        .filter(model.Note.user_id == current_user.id)
        .order_by(model.Note.id.desc())
        .all()
    )
    return [{"id": n.id, "text": n.text} for n in notes]


@router.post("/api/notes")
def api_add_note(
    payload: NoteCreate,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(model.get_db),
):
    """
    AUTH REQUIRED.
    Use `Authorization: Bearer <token>` or `?token=<token>`.
    """
    if not payload.text or not payload.text.strip():
        return {"error": "Text cannot be empty"}

    note = model.Note(user_id=current_user.id, text=payload.text.strip())
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"id": note.id, "text": note.text}


@router.post("/api/notes/delete")
def api_delete_note(
    payload: NoteDelete,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(model.get_db),
):
    """
    AUTH REQUIRED.
    Use `Authorization: Bearer <token>` or `?token=<token>`.
    """
    note = (
        db.query(model.Note)
        .filter(model.Note.id == payload.note_id, model.Note.user_id == current_user.id)
        .first()
    )
    if note is None:
        return {"error": "Note not found"}

    db.delete(note)
    db.commit()
    return {"ok": True}
