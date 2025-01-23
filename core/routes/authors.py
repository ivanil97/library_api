from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.request_schemas import AuthorCreateRequest, AuthorUpdateRequest
from core.response_schemas import AuthorGetResponse
from core.services import AuthorService
from core.utils import get_db_session
from core.utils.role_checker import RoleChecker

router = APIRouter(prefix="/authors", tags=["authors"])
role_checker = Depends(RoleChecker(['admin']))


@router.get("/", response_model=List[AuthorGetResponse], dependencies=[role_checker])
async def get_authors(db: Session = Depends(get_db_session)):
    """
    Эндпойнт для получения списка всех авторов
    """

    author_service = AuthorService(db)
    authors = author_service.get_all_authors()
    return authors


@router.get("/{author_id}", response_model=AuthorGetResponse, dependencies=[role_checker])
async def get_author_by_id(author_id: int,
                           db: Session = Depends(get_db_session)):
    """
    Эндпойнт для получения автора по ID
    """

    author_service = AuthorService(db)
    authors = author_service.get_author_by_id(author_id)
    return authors


@router.post("/", status_code=201, dependencies=[role_checker])
async def create_author(new_author_data: AuthorCreateRequest,
                        db: Session = Depends(get_db_session)):
    """
    Эндпойнт для создания нового автора
    """

    author_service = AuthorService(db)
    new_author = author_service.create_author(new_author_data.model_dump())
    return {"message": "Author added", "author_id": new_author.id}


@router.patch("/{author_id}", dependencies=[role_checker])
async def update_author(updated_author_data: AuthorUpdateRequest,
                        author_id: int,
                        db: Session = Depends(get_db_session)):
    """
    Эндпойнт для обновления данных автора, найденного по ID
    """

    author_service = AuthorService(db)
    target_author = author_service.update_author(author_id, updated_author_data.model_dump(exclude_unset=True))
    return {"message": "Author updated", "author_id": target_author.id}


@router.delete("/{author_id}", dependencies=[role_checker])
async def delete_author(author_id: int,
                        db: Session = Depends(get_db_session)):
    """
    Эндпойнт для удаления автора, найденного по ID
    """

    author_service = AuthorService(db)
    author_service.delete_author(author_id)
    return {"message": "Author and all related books deleted", "author_id": author_id}
