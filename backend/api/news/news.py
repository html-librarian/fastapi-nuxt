from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.news.news import NewsCreate, NewsRead, NewsUpdate, NewsListResponse
from backend.models.news import News, Base
from backend.utils.pagination import get_pagination_params, PaginationParams
from sqlalchemy import create_engine, desc, asc, or_
from sqlalchemy.orm import sessionmaker
import datetime
import os
from backend.config import MEDIA_NEWS_PREVIEW, MEDIA_NEWS_CONTENT, MEDIA_NEWS_CATEGORY, DATABASE_URL
import math
from backend.schemas.news.category import CategoryRead

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ

def validate_image(file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Недопустимый тип файла. Разрешены только изображения.")
    file.file.seek(0, 2)  # Перемещаемся в конец файла
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Слишком большой файл. Максимум 5 МБ.")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/news", tags=["news"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=NewsRead, status_code=status.HTTP_201_CREATED)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    existing = db.query(News).filter(News.slug == news.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Новость с таким slug уже существует")
    now = datetime.datetime.now(datetime.timezone.utc)
    db_news = News(
        title=news.title,
        content=news.content,
        preview=news.preview,
        slug=news.slug,
        category_id=news.category_id,
        created_at=now,
        updated_at=now
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.get("/", response_model=NewsListResponse)
def list_news(
    db: Session = Depends(get_db),
    params: PaginationParams = Depends(get_pagination_params)
):
    query = db.query(News)
    if params.search:
        query = query.filter(
            or_(News.title.ilike(f"%{params.search}%"), News.content.ilike(f"%{params.search}%"))
        )
    total = query.count()
    if params.sort:
        order = desc if params.sort.startswith("-") else asc
        field = params.sort.lstrip("-")
        if hasattr(News, field):
            query = query.order_by(order(getattr(News, field)))
    items = query.offset(params.offset).limit(params.limit).all()
    pages = math.ceil(total / params.limit) if params.limit else 1
    current_page = (params.offset // params.limit) + 1 if params.limit else 1
    next_page = current_page + 1 if current_page < pages else None
    prev_page = current_page - 1 if current_page > 1 else None
    return {
        "items": items,
        "total": total,
        "limit": params.limit,
        "offset": params.offset,
        "pages": pages,
        "next": next_page,
        "prev": prev_page
    }

@router.get("/{news_id}", response_model=NewsRead)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return news

@router.put("/{news_id}", response_model=NewsRead)
def update_news(news_id: int, news_update: NewsUpdate, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    if news_update.title is not None:
        news.title = news_update.title
    if news_update.content is not None:
        news.content = news_update.content
    if news_update.preview is not None:
        news.preview = news_update.preview
    if news_update.slug is not None:
        news.slug = news_update.slug
    if news_update.category_id is not None:
        news.category_id = news_update.category_id
    news.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(news)
    return news

@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    db.delete(news)
    db.commit()

@router.post("/upload-preview/", summary="Загрузка preview для новости")
def upload_preview(file: UploadFile = File(...)):
    validate_image(file)
    filename = file.filename
    file_path = os.path.join(MEDIA_NEWS_PREVIEW, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"preview": f"news/preview/{filename}"}

@router.post("/upload-content/", summary="Загрузка картинки для контента новости")
def upload_content_image(file: UploadFile = File(...)):
    validate_image(file)
    filename = file.filename
    file_path = os.path.join(MEDIA_NEWS_CONTENT, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"url": f"news/content/{filename}"}

@router.post("/categories/upload-image/", summary="Загрузка картинки для категории")
def upload_category_image(file: UploadFile = File(...)):
    validate_image(file)
    filename = file.filename
    file_path = os.path.join(MEDIA_NEWS_CATEGORY, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return {"image": f"news/category/{filename}"} 