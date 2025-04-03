from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:

    @staticmethod
    async def get_user_coins(user_id: int, db: AsyncSession) -> int:
        stmt = text("""
        select balance
        from users
        where id = :user_id
        """)

        result = await db.execute(stmt, {"user_id": user_id})
        # Достаём теперь не кортеж, а именно int - число коинов пользователя
        row = result.fetchone()
        return row[0] if row else 0  # Возвращаем первый элемент кортежа (balance) или 0, если пользователь не найден
