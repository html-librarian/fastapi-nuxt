from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from backend.api.news.news import router as news_router
from backend.api.news.category import router as category_router
import os

app = FastAPI()

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(news_router)
api_router.include_router(category_router)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"} 