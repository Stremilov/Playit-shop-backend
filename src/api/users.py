from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.schemas.users import ExchangeData, ExchangeResponse
from src.core.services.prizes import PrizeService

users_router = APIRouter(
    prefix="",
    tags=["Prizes"]
)


@users_router.post(
    path="/exchange",
    response_model=ExchangeResponse,
    summary="Обменивает коины пользователя на приз",
    description="""
    Позволяет обменять коины пользователя на призы
    
    - Аутентифицирует пользователя по jwt токену
    - Уменьшает баланс пользователя на число равное цене приза
    - Убавляет количество вещи, которую получает пользователь на 1
    - Добавляет приз пользователю
    - Делает запись транзакции в бд
    """
)
async def change_user_points(
        request: Request,
        data: ExchangeData,
        db: AsyncSession = Depends(get_db)
):
    return await PrizeService.exchange(request=request, data=data, db=db)
