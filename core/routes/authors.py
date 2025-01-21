from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.database import session
from core.request_schemas import AuthorCreateRequest, AuthorUpdateRequest
from core.response_schemas import AuthorGetResponse
from core.models import Author as AuthorModelDB

from core.utils.role_checker import RoleChecker

router = APIRouter(prefix="/authors", tags=["authors"])
role_checker = Depends(RoleChecker(['admin']))


@router.get("/", response_model=List[AuthorGetResponse], dependencies=[role_checker])
async def get_authors():
    all_authors = session.execute(select(AuthorModelDB)).scalars().all()
    if not all_authors:
        raise HTTPException(status_code=404, detail="No authors found")
    return all_authors


@router.get("/{author_id}", response_model=AuthorGetResponse)
async def get_author_by_id(author_id: int):
    statement = select(AuthorModelDB).where(AuthorModelDB.id == author_id).options(joinedload(AuthorModelDB.books))
    result = session.execute(statement).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        return result


@router.post("/", status_code=201)
async def create_author(new_author: AuthorCreateRequest):
    new_author_db = AuthorModelDB(
        name=new_author.name,
        bio=new_author.bio,
        birthday=new_author.birthday
    )

    session.add(new_author_db)
    session.commit()
    session.refresh(new_author_db)

    return {"message": "Author added", "author_id": new_author_db.id}


@router.patch("/{author_id}")
async def update_author(author_id: int, author: AuthorUpdateRequest):
    statement = select(AuthorModelDB).where(AuthorModelDB.id == author_id).options(joinedload(AuthorModelDB.books))
    target_author = session.execute(statement).scalars().first()

    if not target_author:
        raise HTTPException(status_code=404, detail="Book not found")

    new_data = author.model_dump(exclude_unset=True)

    for author_property, new_value in new_data.items():
        setattr(target_author, author_property, new_value)

    session.commit()

    return {"message": "Author updated", "author_id": target_author.id}


@router.delete("/{author_id}")
async def delete_author(author_id: int):
    statement = select(AuthorModelDB).where(AuthorModelDB.id == author_id)
    target_author = session.execute(statement).scalars().first()

    if not target_author:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        session.delete(target_author)
        session.commit()

        # удаляем все книги автора
        for i_book in target_author.books:
            session.delete(i_book)
        session.commit()

        return {"message": "Author and all related books deleted", "author_id": author_id}
