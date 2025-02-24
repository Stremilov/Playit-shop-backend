from fastapi import HTTPException, Request

from src.core.jwt.tokens import verify_jwt_token


async def verify_user_by_jwt(request: Request):
    """
    Возвращает пользователя после аутентификации по username с помощью jwt
    """
    token = request.cookies.get("jwt-token")
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован")

    verified_token = verify_jwt_token(token)

    telegram_id = verified_token.get("telegram_id")
    return UserRepository.get_user_by_telegram_id(telegram_id=telegram_id)
