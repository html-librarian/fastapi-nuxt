from fastapi import Query, Depends
from typing import Optional

class PaginationParams:
    def __init__(
        self,
        limit: int = Query(10, ge=1, le=100, description="Сколько элементов вернуть"),
        offset: int = Query(0, ge=0, description="Сколько элементов пропустить"),
        sort: Optional[str] = Query(None, description="Поле для сортировки, например: 'created_at' или '-created_at'"),
        search: Optional[str] = Query(None, description="Поисковый запрос по заголовку или содержимому")
    ):
        self.limit = limit
        self.offset = offset
        self.sort = sort
        self.search = search

def get_pagination_params(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
) -> PaginationParams:
    return PaginationParams(limit, offset, sort, search) 