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
            # Проверяем, не начата ли уже транзакция
            if db.in_transaction():
                # Если транзакция уже начата, работаем без контекстного менеджера
                try:
                    return await PrizeRepository._perform_exchange_operations(
                        prize_title, prize_value, user_id, db
                    )
                except Exception as e:
                    await db.rollback()
                    logging.error(f"Ошибка при обмене (вложенная транзакция): {e}", exc_info=True)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ошибка при обмене: {str(e)}"
                    )
            else:
                # Если транзакции нет, используем контекстный менеджер
                try:
                    async with db.begin():
                        result =  await PrizeRepository._perform_exchange_operations(
                            prize_title, prize_value, user_id, db
                        )
                        await db.commit()
                        return result
                except Exception as e:
                    logging.error(f"Ошибка при обмене (новая транзакция): {e}", exc_info=True)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ошибка при обмене: {str(e)}"
                    )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в PrizeRepository.exchange: {str(e)}")

    @staticmethod
    async def _perform_exchange_operations(prize_title: str, prize_value: int, user_id: int, db: AsyncSession):
        """Выполнение операций обмена"""
        try:
            # 1. Проверка баланса
            balance_result = await db.execute(
                text("SELECT balance FROM users WHERE id = :user_id FOR UPDATE"),
                {"user_id": user_id}
            )
            balance = balance_result.scalar()

            if balance is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            if balance < prize_value:
                raise HTTPException(status_code=400, detail="Недостаточно средств")

            # 2. Добавление приза
            await db.execute(
                text("""
                    INSERT INTO prizes (title, value, user_id)
                    VALUES (:title, :value, :user_id)
                """),
                {"title": prize_title, "value": prize_value, "user_id": user_id}
            )

            # 3. Обновление баланса
            await db.execute(
                text("""
                    UPDATE users
                    SET balance = balance - :value
                    WHERE id = :user_id
                """),
                {"value": prize_value, "user_id": user_id}
            )

            await db.commit()

            # 4. Получение обновленных данных
            user_result = await db.execute(
                text("SELECT * FROM users WHERE id = :user_id"),
                {"user_id": user_id}
            )
            user_row = user_result.fetchone()
            user_dict = dict(user_row._mapping) # для перевода в _mapping ля перевода в словарь

            return ExchangeResponse(
                status="success",
                details="Обмен произведен",
                user=user_dict
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка в PrizeRepository._perform_exchange_operations: {str(e)}")