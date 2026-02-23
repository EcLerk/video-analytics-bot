from aiogram import Router
from aiogram.types import Message
from app.llm.openai_llm import text_to_sql
from app.llm.db_query import execute_query

router = Router()


@router.message()
async def handle_message(message: Message) -> None:
    await message.answer("Обрабатываю запрос...")

    try:
        sql = await text_to_sql(message.text)
        result = await execute_query(sql)
    except Exception as e:
        await message.answer(f"Ошибка выполнения запроса: {e}")

    await message.answer(f"Результат: {result}")