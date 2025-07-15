from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.models.news import Category, Base
from backend.schemas.news.category import CategoryCreate, CategoryRead, CategoryListResponse
from backend.config import MEDIA_NEWS_CATEGORY, DATABASE_URL
from backend.utils.pagination import get_pagination_params, PaginationParams
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
import os
import math

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/categories", tags=["categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=CategoryListResponse)
def list_categories(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(get_pagination_params)
):
    query = db.query(Category)
    total = query.count()
    items = query.offset(params.offset).limit(params.limit).all()
    return {
        "items": items,
        "total": total,
        "limit": params.limit,
        "offset": params.offset
    } 