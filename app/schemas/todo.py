from typing import Optional

from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool

    class Config:
        from_attributes = True