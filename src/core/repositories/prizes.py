import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from src.core.schemas.users import ExchangeResponse


class PrizeRepository:

    @staticmethod
    async def exchange(prize_title: str, prize_value: int, user_id: int, db: AsyncSession):
        try:
            async with db.begin():
                stmt = text(f"""
                            insert into prizes (title, value, user_id) values (:title, :value, :user_id)
                        """)

                logging.info("Добавление приза пользователю")
                await db.execute(stmt, {"title": prize_title, "value": prize_value, "user_id": user_id})

                stmt = text(f"""
                    update users
                    set balance = balance - :value
                    where id = :user_id
                """)
    
                logging.info("Обновление баланса пользователя")
                await db.execute(stmt, {"value": prize_value, "user_id": user_id})

                stmt = text(f"""
                    select * from users where id = :user_id
                """)

                logging.info("Получение пользователя")
                result = await db.execute(stmt, {"user_id": user_id})
                user = result.fetchone()

                await db.commit()
        except Exception as e:
            await db.rollback()
            logging.error(f"Ошибка при обмена валюты на приз. Ошибка: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Ошибка при обмена валюты на приз. Ошибка: {e}")

        return ExchangeResponse(
            status="success",
            details="Обмен произведен и приз добавлен пользователю",
            user=user
        )
