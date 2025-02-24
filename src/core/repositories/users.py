from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:

    @staticmethod
    async def get_user_coins(user_id: int, db: AsyncSession):
        stmt = text("""
        select balance
        from users
        where user_id = :user_id
        """)

        result = await db.execute(stmt, {"user_id": user_id})
        return result.fetchone()
