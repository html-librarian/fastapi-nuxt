# FastAPI Backend — Новости и Категории

## Быстрый старт

1. **Создай и активируй виртуальное окружение:**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Установи зависимости:**

```bash
pip install -r requirements.txt
```

3. **Запусти сервер:**

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Открой в браузере:**

- [http://localhost:8000/docs](http://localhost:8000/docs) — Swagger UI
- [http://localhost:8000/api/v1/news/](http://localhost:8000/api/v1/news/) — CRUD новости
- [http://localhost:8000/api/v1/categories/](http://localhost:8000/api/v1/categories/) — CRUD категории
- [http://localhost:8000/media/news/preview/имя_файла](http://localhost:8000/media/news/preview/имя_файла) — доступ к медиа

---

## Основные возможности

- **CRUD для News и Category** (создание, получение, обновление, удаление)
- **Связь News → Category** (один-ко-многим)
- **Загрузка медиафайлов:**
  - preview для новости (`/api/v1/news/upload-preview/`)
  - картинки для контента (`/api/v1/news/upload-content/`)
  - картинка для категории (`/api/v1/categories/upload-image/`)
- **Раздача медиа** через `/media/...`
- **Slug** для News и Category (уникальный, поддержка кириллицы)
- **Pydantic-схемы** для всех сущностей, поддержка списков с пагинацией, сортировкой, поиском
- **Структура ответа для списков:**
  ```json
  {
    "items": [...],
    "total": 100,
    "limit": 10,
    "offset": 0,
    "pages": 10,
    "next": 1,
    "prev": null
  }
  ```
- **Валидация файлов** (тип, размер)
- **Централизованные настройки** в `config.py`
- **Версионирование API** (`/api/v1/`)

---

## Работа с миграциями (Alembic)

1. **Инициализация (один раз):**
   ```bash
   alembic init alembic
   ```
2. **Создать миграцию:**
   ```bash
   alembic revision --autogenerate -m "init"
   ```
3. **Применить миграции:**
   ```bash
   alembic upgrade head
   ```
4. **Для dev-режима:**
   Можно удалить файл БД и пересоздать миграции при изменении моделей.

---

## Важно

- Все API доступны только по префиксу `/api/v1/`
- Медиафайлы доступны по `/media/...`
- Для корректной работы среды разработки:
  - Активируй venv перед запуском
  - В VSCode выбери Python-интерпретатор из venv
  - Если видишь ошибки импортов — перезапусти VSCode и проверь настройки

---

Проект создан на базе [FastAPI](https://fastapi.tiangolo.com/).
