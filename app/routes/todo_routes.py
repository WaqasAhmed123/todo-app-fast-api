from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.todo_respository import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse
from app.services.jwt_service import get_current_user

todo_router = APIRouter(prefix="/todos", tags=["Todos"])

repository = TodoRepository()

@todo_router.get("/", response_model=List[TodoResponse])
def get_all_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repository.get_all_todos(db)

@todo_router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return repository.create_todo(db, todo.title, user_id=current_user["id"], description=todo.description)