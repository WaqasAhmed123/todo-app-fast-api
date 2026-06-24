from sqlalchemy.orm import Session

from app.models.todo import Todo


class TodoRepository:
    def get_all_todos(self, db: Session):
        return db.query(Todo).all()

    def create_todo(self, db: Session, title: str):
        new_todo = Todo(title=title)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
