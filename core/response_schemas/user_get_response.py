from pydantic import BaseModel


class UserGetResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на получение пользователя
    """

    id: int
    first_name: str
    last_name: str
    email: str
