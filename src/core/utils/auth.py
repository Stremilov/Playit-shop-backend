from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt.tokens import verify_jwt_token
from src.core.repositories.users import UserRepository


async def verify_user_by_jwt(request: Request, session: AsyncSession):
    """
    Возвращает пользователя после аутентификации по username с помощью jwt
    """
    token = request.cookies.get("jwt-token")
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")

    verified_token = verify_jwt_token(token)

    tg_from_jwt = verified_token.get("telegram_id")
    print(tg_from_jwt)
    username_from_db = UserRepository.get_user_by_tg_id(db=session, tg_id=tg_from_jwt)
    if not username_from_db:
        raise HTTPException(status_code=401, detail="По такому имени в JWT-Токене нет пользователя в базе данных")

