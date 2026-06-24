from fastapi import FastAPI
from app.routes.todo_routes import router
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
