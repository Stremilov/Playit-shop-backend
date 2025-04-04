from fastapi_users.jwt import decode_jwt
from fastapi import HTTPException
from src.core.utils.config import settings


def verify_jwt_token(token: str) -> dict:
    """
    Синхронно декодирует и проверяет JWT-токен.
    """
    # try:
    audience = "prod"  # Должно совпадать с "aud" в create_jwt_token
    d_token = decode_jwt(str(token), settings.token.SECRET_KEY, audience)
    print(d_token)
    # return decode_jwt(str(token), settings.token.SECRET_KEY, audience)
    return d_token
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail=f"Невалидный токен: {str(e)}")
