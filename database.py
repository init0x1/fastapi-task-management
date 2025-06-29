from sqlmodel import SQLModel, create_engine, Session
from typing import Generator


DATABASE_URL = "sqlite:///./tasks.db"


engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  
    echo=True   
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session 