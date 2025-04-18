from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.prizes import PrizeRepository
from src.core.repositories.users import UserRepository
from src.core.schemas.users import ExchangeData
from src.core.services.excel import ExcelService
from src.core.utils.auth import verify_user_by_jwt


class PrizeService:

    @staticmethod
    async def exchange(request: Request, data: ExchangeData, db: AsyncSession):
        try:
            await verify_user_by_jwt(request=request, session=db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при верификации по jwt-Токену: {str(e)}")

        # Ранее тут сравнивался tuple с числом, исправил это в get_user_coins(...)
        try:
            if await UserRepository.get_user_coins(user_id=data.user_id, db=db) >= data.value:
                # TODO подумать над реализацией потому что ExcelService.decrement_prize_count может выполнится,
                #  а PrizeRepository.exchange может не выполниться и мы потеряем 1 значение количества вещи
                await ExcelService.decrement_prize_count(request, item_name=data.prize_title)
                return await PrizeRepository.exchange(prize_title=data.prize_title, prize_value=data.value,
                                                      user_id=data.user_id, prize_id=data.prize_id, db=db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в PrizeService.exchange {str(e)}")
