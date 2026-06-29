from fastapi import FastAPI
from app.routes.todo_routes import todo_router
from app.routes.auth_routes import auth_router
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)