from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    content: str
    preview: Optional[str] = None
    slug: str
    category_id: int

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    preview: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None

class NewsRead(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NewsListResponse(BaseModel):
    items: List[NewsRead]
    total: int
    limit: int
    offset: int
    pages: int
    next: Optional[int]
    prev: Optional[int] 