from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(todos)")).fetchall()
        if rows and "completed_by" not in {row[1] for row in rows}:
            conn.execute(
                text("ALTER TABLE todos ADD COLUMN completed_by INTEGER REFERENCES users(id)")
            )
