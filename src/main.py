import asyncio

from app.bot.router import router
from app.config.settings import settings
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(token=settings.tg_bot_settings.api_key)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
