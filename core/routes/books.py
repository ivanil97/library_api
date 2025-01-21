from sqlalchemy.orm import joinedload

from core.models import Book as BookModelDB, Author as AuthorModelDB
from sqlalchemy import select
from typing import List, Annotated

from core.database import session

from fastapi import APIRouter, HTTPException, Depends

from core.request_schemas import BookCreateRequest, BookUpdateRequest
from core.response_schemas import BookGetResponse
from core.utils.get_current_user import get_current_user
from core.utils.role_checker import RoleChecker

router = APIRouter(prefix="/books", tags=["books"])

user_dependency = Annotated[dict, Depends(get_current_user)]
role_checker = Depends(RoleChecker(['admin']))


# TODO: проверить, если user_dependency будет в декораторе
@router.get("/", response_model=List[BookGetResponse])
async def get_books(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    all_books = session.execute(select(BookModelDB)).scalars().all()
    if not all_books:
        raise HTTPException(status_code=404, detail="No books found")
    return all_books


@router.get("/{book_id}", status_code=200, response_model=BookGetResponse)
async def get_book_by_id(book_id: int):
    statement = select(BookModelDB).where(BookModelDB.id == book_id).options(joinedload(BookModelDB.authors))
    result = session.execute(statement).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return result


@router.post("/", status_code=201, dependencies=[role_checker])
async def create_book(new_book: BookCreateRequest):
    authors_data = session.execute(select(AuthorModelDB)).scalars().all()
    existing_authors = {i_author.name: i_author for i_author in authors_data}
    new_book_authors = []

    for i_author in new_book.authors:
        # проверяем уникальность автора по имени, чтобы не создавать нового
        if i_author.name in existing_authors:
            new_author = existing_authors[i_author.name]
        else:
            new_author = AuthorModelDB(
                name=i_author.name,
                bio=i_author.bio,
                birthday=i_author.birthday,
            )
            session.add(new_author)
        new_book_authors.append(new_author)
    session.commit()

    new_book_db = BookModelDB(
        title=new_book.title,
        description=new_book.description,
        publication_date=new_book.publication_date,
        authors=new_book_authors,
        genres=new_book.genres,
        quantity_available=new_book.quantity_available
    )

    session.add(new_book_db)
    session.commit()
    session.refresh(new_book_db)

    return {"message": "Book added", "book_id": new_book_db.id}


@router.patch("/{book_id}", status_code=201, dependencies=[role_checker])
async def update_book(book_id: int, book: BookUpdateRequest):
    statement = select(BookModelDB).where(BookModelDB.id == book_id).options(joinedload(BookModelDB.authors))
    target_book = session.execute(statement).scalars().first()

    if not target_book:
        raise HTTPException(status_code=404, detail="Book not found")

    new_data = book.model_dump(exclude_unset=True)

    authors_data = session.execute(select(AuthorModelDB)).scalars().all()
    existing_authors = {i_author.name: i_author for i_author in authors_data}

    for book_property, new_value in new_data.items():
        if book_property == "authors":
            # Обновляем авторов, если переданы новые данные
            target_book.authors = []
            for i_author in new_value:
                if i_author.name in existing_authors:
                    new_author = existing_authors[i_author.name]
                else:
                    new_author = AuthorModelDB(
                        name=i_author['name'],
                        bio=i_author['bio'],
                        birthday=i_author['birthday']
                    )
                    session.add(new_author)
                target_book.authors.append(new_author)
        else:
            setattr(target_book, book_property, new_value)

    session.commit()

    return {"message": "Book updated", "book_id": target_book.id}


@router.delete("/{book_id}", status_code=200, dependencies=[role_checker])
async def delete_book(book_id: int):
    statement = select(BookModelDB).where(BookModelDB.id == book_id)
    target_book = session.execute(statement).scalars().first()

    if not target_book:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        session.delete(target_book)
        session.commit()

        return {"message": "Book deleted", "book_id": book_id}
