# COMP6300

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
│   └── users.html
└── app.db   (created automatically)
```

## 0. Create the app Directory if not already created

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
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart pydantic[email]
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
from sqlalchemy import create_engine, Column, Integer, String
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
```

controller.py

```python
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

```

main.py

```python
from fastapi import FastAPI
import uvicorn

import model
from controller import router

app = FastAPI()

@app.on_event("startup")
def startup():
    model.init_db()

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        reload=True
    )
```

templates/users.html

```html
<!doctype html>
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
