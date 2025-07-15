from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    image: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryListResponse(BaseModel):
    items: List[CategoryRead]
    total: int
    limit: int
    offset: int 