from typing import Optional

from sqlalchemy.orm import Session

from app.models.todo import Todo


class TodoRepository:
    
    def get_all_todos(self, db: Session):
        # Logic to retrieve all todos from the database
        return db.query(Todo).all()
    
    def create_todo(self, db: Session, title: str, user_id: int, description: Optional[str] = None):
        # Logic to create a new todo in the database
        new_todo = Todo(title=title, description=description, user_id=user_id)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo