# COMP6300

Week 4 Lab: Implement SSR, REST API endpoints, DB read/write, and Pydantic schema validation

**Model–View–Controller** setup in FastAPI using **server-side rendered HTML (Jinja2)** with only:

- `model.py` (SQLAlchemy + DB session)
- `view.py` (template rendering)
- `controller.py` (routes)
- `main.py` (Application entry point) (`python main.py`)
- `templates/` (your actual HTML)

---

## Folder layout

```
app/
├── venv/
├── main.py
├── model.py
├── view.py
├── controller.py
├── templates/
│   ├── users.html
│   └── user2.html
└── app.db   (created automatically)
```

Teaching note:
- `app.db` is created automatically and will include tables: `users`, `user_credentials`, and `notes`.

## 0. Create the app Directory if not already created

Ensure you are within the app directory after creation, all operations including run via terminal takes place within the app directory.

```bash
mkdir app
cd app

```

---

## 1. First: Create a virtual environment (`venv`)

A **virtual environment** keeps your project’s Python packages isolated from the rest of your system, so different projects can use different versions of libraries without conflicts.

From inside your project folder, run:

```bash
python -m venv venv
```

This creates a new folder called `venv` that contains an isolated Python environment.

If your system uses `python3` instead, you would run:

```bash
python3 -m venv venv
```

---

## 2. Second: Activate and deactivate the virtual environment

You should **activate** the virtual environment before installing packages or running your app, so everything is installed into `venv`.

### 2.1 Activate on Windows

- **PowerShell**:

  ```bash
  .\venv\Scripts\Activate.ps1
  ```

- **Command Prompt (cmd.exe)**:

  ```bash
  venv\Scripts\activate
  ```

You should see something like `(venv)` appear at the start of your terminal prompt, indicating that the virtual environment is active.

### 2.2 Activate on macOS / Linux

```bash
source venv/bin/activate
```

Again, you should see `(venv)` at the beginning of your prompt.

### 2.3 Deactivate the virtual environment (all platforms)

To deactivate (go back to the system Python), simply run:

```bash
deactivate
```

After this, the `(venv)` prefix will disappear from your prompt.

---

## 3. Third Install libraries

```bash
# Added in this lab extension:
# - PyJWT: issue + verify JWT tokens for login/register
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart pydantic[email] pyjwt
```

## 4. Create the Templates Folder

```bash
mkdir templates

```

## 5. Create the Python Files

Inside the `app/` directory, create:

```css
main.py
model.py
view.py
controller.py
```

### 📄 Add the Code

model.py

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class UserCredential(Base):
    """
    Teaching note:
    We keep the original `users` table unchanged and store passwords separately.
    """

    __tablename__ = "user_credentials"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    password_hash = Column(String, nullable=False)


class Note(Base):
    """
    Per-user note items (used for authenticated CRUD).
    """

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    text = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

view.py

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def render_users(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request},
    )

def render_users2(request: Request):
    return templates.TemplateResponse(
        "user2.html",
        {"request": request},
    )
```

controller.py

```python
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
import os
import jwt

import model
import view

router = APIRouter()

# JWT configuration (teaching)
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
bearer_scheme = HTTPBearer(auto_error=False)


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


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(model.get_db),
) -> model.User:
    """
    AUTH REQUIRED dependency.

    Send token via:
    - Authorization: Bearer <token>   (standard)
    - OR ?token=<token>               (teaching / quick testing)
    """

    token = credentials.credentials if credentials else None
    if not token:
        token = request.query_params.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token. Send Authorization: Bearer <token> or ?token=<token>",
        )

    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    user_id = int(payload["sub"])
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


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


# ... plus: GET/PUT/DELETE /api/users/{user_id} ...
# ... plus: POST /api/register and POST /api/login (issue JWTs) ...


@router.get("/api/me")
def api_me(current_user: model.User = Depends(get_current_user)):
    """AUTH REQUIRED."""
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}


@router.get("/api/notes")
def api_list_notes(
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(model.get_db),
):
    """AUTH REQUIRED."""
    notes = db.query(model.Note).filter(model.Note.user_id == current_user.id).all()
    return [{"id": n.id, "text": n.text} for n in notes]


@router.post("/api/notes")
def api_add_note(
    payload: NoteCreate,
    current_user: model.User = Depends(get_current_user),
    db: Session = Depends(model.get_db),
):
    """AUTH REQUIRED."""
    note = model.Note(user_id=current_user.id, text=payload.text)
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
    """AUTH REQUIRED."""
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

```

main.py

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

import model
from controller import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    model.init_db()
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
```

templates/users.html

```html
<!doctype html>
<!-- this file will be server side rendered by the fastapi backend, and will be used to display the list of users and a form to add new users. It will also include some client-side JavaScript to handle form submission and fetching the list of users from the backend API. -->
<html>
  <body>
    <h1>Users</h1>

    <form id="userForm">
      <input id="name" placeholder="name" required />
      <input id="email" placeholder="email" required />
      <button type="submit">Add</button>
    </form>

    <p id="error" style="color:red;"></p>

    <hr />
    <ul id="userList"></ul>

    <script>
      async function loadUsers() {
        const res = await fetch("/api/users");
        const users = await res.json();

        const list = document.getElementById("userList");
        list.innerHTML = "";

        users.forEach((u) => {
          const li = document.createElement("li");
          li.textContent = `${u.id} — ${u.name} (${u.email})`;
          list.appendChild(li);
        });
      }

      document
        .getElementById("userForm")
        .addEventListener("submit", async (e) => {
          e.preventDefault();

          const payload = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
          };

          const res = await fetch("/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });

          const data = await res.json();

          if (data.error) {
            document.getElementById("error").textContent = data.error;
            return;
          }

          document.getElementById("error").textContent = "";
          e.target.reset();
          loadUsers();
        });

      loadUsers();
    </script>
  </body>
</html>
```

## 6. Run the Application

Make sure:

- You are inside `app/`
- The virtual environment is activated

Then run:

```bash
python main.py
```

Open:

```
http://127.0.0.1:8080/users
```

### To Understand:

- **Model**: defines data + DB session
- **Controller**: handles HTTP, reads form fields, calls DB, returns view
- **View**: renders HTML templates and receives data from controller

---

## Week 4 extension: Register/Login (JWT) + Authenticated Notes

This repo now also includes a minimal example of:

- **Register** a user and store a **password hash** (never store raw passwords)
- **Login** to receive a **JWT token**
- Call **authenticated endpoints** by sending:
  - `Authorization: Bearer <token>`
  - (teaching fallback) or add `?token=<token>` to the URL

### New pages

- `GET /users2`:
  - A teaching UI (`templates/user2.html`) to register/login and create/delete notes

### New database tables (created automatically)

We **keep the original `users` table**. Two extra tables are added:

- `user_credentials`:
  - Stores password hashes (one row per user)
- `notes`:
  - Stores per-user note items (used to demonstrate authenticated CRUD)

If you already have an old `app.db`, these new tables will be created on startup.
Existing users that were created before this extension will not have passwords set.

### Auth endpoints

- `POST /api/register`
  - body: `{ "name": "...", "email": "...", "password": "..." }`
  - returns: `{ token, token_type, user }`
- `POST /api/login`
  - body: `{ "email": "...", "password": "..." }`
  - returns: `{ token, token_type, user }`
- `GET /api/me` (**auth required**)
  - returns the current user extracted from the token

### User CRUD endpoints

- `GET /api/users`
- `POST /api/users`
- `GET /api/users/{user_id}`
- `PUT /api/users/{user_id}`
- `DELETE /api/users/{user_id}`

### Notes endpoints (auth required)

These require the JWT token in the request header.

- `GET /api/notes`
- `POST /api/notes`
  - body: `{ "text": "..." }`
- `POST /api/notes/delete`
  - body: `{ "note_id": 123 }`

### JWT secret (important)

For teaching, the app defaults to a dev secret, but you can (and should) set your own.

In **production**, teams commonly store secrets in a **`.env` file** (or a secret manager) and load them into environment variables (for example using `python-dotenv`). We **do not enforce** `.env` in this repo—this app simply reads `JWT_SECRET` directly from the environment.

- PowerShell:

```bash
$env:JWT_SECRET="a-long-random-secret"
python main.py
```
