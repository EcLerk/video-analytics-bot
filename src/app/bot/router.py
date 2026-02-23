import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.services.llm import text_to_sql
from app.services.db_query import execute_query
from app.exceptions.exceptions import LLMError, DatabaseQueryError, UnsafeSQLError, NotFoundError

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    await message.answer(
        "👋 Привет! Я аналитический бот.\n\n"
        "Задавай вопросы о видео на русском языке, например:\n"
        "— Сколько всего просмотров у всех видео?\n"
        "— У каких креаторов есть видео с 1 по 5 ноября 2025?\n"
        "— Какой прирост лайков был за ноябрь?"
    )


@router.message()
async def handle_message(message: Message) -> None:
    processing_msg = await message.answer("⏳ Обрабатываю запрос...")

    try:
        sql = await text_to_sql(message.text)
        logger.info("Generated SQL: %s", sql)
        result = await execute_query(sql)
        await processing_msg.delete()
        await message.answer(f"📊 Результат: {result}")

    except UnsafeSQLError:
        logger.warning("Unsafe SQL generated for message: %s", message.text)
        await processing_msg.edit_text("❌ Не удалось безопасно обработать запрос, попробуй переформулировать")

    except LLMError:
        logger.error("LLM failed to process message: %s", message.text)
        await processing_msg.edit_text("❌ Сервис временно недоступен, попробуй позже")

    except DatabaseQueryError:
        logger.error("DB query failed for message: %s", message.text)
        await processing_msg.edit_text("❌ Ошибка при выполнении запроса к базе данных")

    except NotFoundError:
        await processing_msg.edit_text("🔍 По вашему запросу ничего не найдено")