from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.prizes import PrizeRepository
from src.core.repositories.users import UserRepository
from src.core.schemas.users import ExchangeData
from src.core.services.excel import ExcelService


class PrizeService:

    @staticmethod
    async def exchange(request: Request, data: ExchangeData, db: AsyncSession):
        if await UserRepository.get_user_coins(user_id=data.user_id, db=db) >= data.value:
            # TODO подумать над реализацией потому что ExcelService.decrement_prize_count может выполнится,
            #  а PrizeRepository.exchange может не выполниться и мы потеряем 1 значение количества вещи
            await ExcelService.decrement_prize_count(request, item_name=data.prize_title)
            return await PrizeRepository.exchange(prize_title=data.prize_title, prize_value=data.value,
                                                  user_id=data.user_id, db=db)
