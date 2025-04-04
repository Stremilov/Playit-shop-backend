from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class UserRepository:

    @staticmethod
    async def get_user_coins(user_id: int, db: AsyncSession) -> int:
        stmt = text("""
        select balance
        from users
        where id = :user_id
        """)
        try:
            result = await db.execute(stmt, {"user_id": user_id})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе в БД {str(e)}")
        # Достаём теперь не кортеж, а именно int - число коинов пользователя
        row = result.fetchone()
        return row[0] if row else 0  # Возвращаем первый элемент кортежа (balance) или 0, если пользователь не найден

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[str]:
        stmt = text("""
                    select username
                    from users
                    where username = :username
                    """)
        # try:
        result = await db.execute(stmt, {"username": username})
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Ошибка при запросе в БД {str(e)}")

        row = result.fetchone()

        return row[0] if row else None


