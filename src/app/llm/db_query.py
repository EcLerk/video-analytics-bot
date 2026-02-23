from sqlalchemy import text
from app.db.session import Session


async def execute_query(sql: str) -> str:
    async with Session() as session:
        try:
            result = await session.execute(text(sql))
            row = result.fetchone()
            if row is None:
                return "Данные не найдены"
            return str(row[0])
        except Exception as e:
            return f"Ошибка выполнения запроса: {e}"