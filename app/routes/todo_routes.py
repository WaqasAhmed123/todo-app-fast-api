from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.todo_respository import TodoRepository


router = APIRouter(prefix="/todos", tags=["Todos"])

repository = TodoRepository()

@router.get("/")
def get_all_todos(db : Session = Depends(get_db)):
    return repository.get_all_todos(db)

@router.post("/")
def create_todo(title: str, db: Session = Depends(get_db)):
    return repository.create_todo(db, title)