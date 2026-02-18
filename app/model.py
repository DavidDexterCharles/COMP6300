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
    We keep the original `users` table unchanged and store passwords in a separate table.
    This helps show separation of concerns:
    - `users` = public profile data (name/email)
    - `user_credentials` = authentication secrets (password hashes)
    """

    __tablename__ = "user_credentials"

    # One-to-one with `users` (a user has exactly one credential record)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # We store a *hash*, never the raw password.
    password_hash = Column(String, nullable=False)


class Note(Base):
    """
    A simple per-user "item" (note) table used to demonstrate authenticated endpoints.
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