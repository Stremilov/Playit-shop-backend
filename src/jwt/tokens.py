from datetime import datetime, timedelta
from fastapi_users.jwt import generate_jwt, decode_jwt
from fastapi import HTTPException
from src.utils.config import SECRET_KEY


def verify_jwt_token(token: str) -> dict:
    """
    Синхронно декодирует и проверяет JWT-токен.
    """
    try:
        audience = "prod"
        return decode_jwt(token, SECRET_KEY, audience)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Невалидный токен: {str(e)}")