import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
MEDIA_NEWS = os.path.join(MEDIA_ROOT, "news")
MEDIA_NEWS_PREVIEW = os.path.join(MEDIA_NEWS, "preview")
MEDIA_NEWS_CONTENT = os.path.join(MEDIA_NEWS, "content")
MEDIA_NEWS_CATEGORY = os.path.join(MEDIA_NEWS, "category")
os.makedirs(MEDIA_NEWS, exist_ok=True)
os.makedirs(MEDIA_NEWS_PREVIEW, exist_ok=True)
os.makedirs(MEDIA_NEWS_CONTENT, exist_ok=True)
os.makedirs(MEDIA_NEWS_CATEGORY, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'app.db')}" 