from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends


from core.models import User as UserModelDB
from core.services import UserAuthService, OperationService
from core.utils import get_db_session


router = APIRouter(prefix="/operations", tags=["operations"])


@router.patch('/book_lending')
async def book_lend(book_id: int,
                    db: Session = Depends(get_db_session),
                    current_user: UserModelDB = Depends(UserAuthService.get_current_user)):
    """
    Эндпоинт для выдачи книг читателю
    """

    operation_services = OperationService(db)
    result = operation_services.lend_book(current_user, book_id)
    return result


@router.patch('/book_returning')
async def book_return(book_id: int,
                      db: Session = Depends(get_db_session),
                      current_user: UserModelDB = Depends(UserAuthService.get_current_user)):
    """
    Эндпоинт для возврата книг от читателя
    """

    operation_services = OperationService(db)
    result = operation_services.return_book(current_user, book_id)
    return result
