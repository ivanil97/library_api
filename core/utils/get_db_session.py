from core.database import Session


def get_db_session():
    """
    Возвращает инстанс базы данных
    """

    db = None
    try:
        db = Session()
        yield db
    finally:
        db.close()
