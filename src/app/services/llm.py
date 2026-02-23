from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.settings import settings
from app.exceptions.exceptions import LLMError

client = AsyncOpenAI(
    api_key=settings.openai_settings.api_key,
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
Ты — аналитик данных. Тебе дана схема базы данных PostgreSQL.

Таблица videos:
- id (UUID) — уникальный идентификатор видео
- creator_id (str) — идентификатор автора
- video_created_at (timestamptz) — дата публикации видео
- views_count (int) — текущее количество просмотров
- likes_count (int) — текущее количество лайков
- comments_count (int) — текущее количество комментариев
- reports_count (int) — текущее количество жалоб
- created_at (timestamptz) — дата добавления записи в БД
- updated_at (timestamptz) — дата последнего обновления записи

Таблица snapshots — исторические срезы метрик видео, создаются периодически:
- id (UUID) — уникальный идентификатор снапшота
- video_id (UUID) — ссылка на videos.id
- views_count (int) — просмотры на момент снапшота
- likes_count (int) — лайки на момент снапшота
- comments_count (int) — комментарии на момент снапшота
- reports_count (int) — жалобы на момент снапшота
- delta_views_count (int) — прирост просмотров с предыдущего снапшота
- delta_likes_count (int) — прирост лайков с предыдущего снапшота
- delta_comments_count (int) — прирост комментариев с предыдущего снапшота
- delta_reports_count (int) — прирост жалоб с предыдущего снапшота
- created_at (timestamptz) — дата создания снапшота

Правила:
- Текущие значения метрик (сколько просмотров у видео) — берутся из таблицы videos
- Исторические данные и приросты — из таблицы snapshots
- Всегда возвращай ТОЛЬКО один SQL-запрос без пояснений, без markdown, без ```sql
- Запрос должен возвращать ровно одно число
- Используй только SELECT, никаких INSERT/UPDATE/DELETE
- Все временные условия указывай в UTC (+00), так как именно в этом timezone корректно работают сравнения
- Пример: "с 10:00 до 15:00 28 ноября" →
  created_at >= '2025-11-28 10:00:00+00' AND created_at <= '2025-11-28 15:00:00+00'
- Убери правило про +03, всегда используй +00
"""


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def text_to_sql(user_message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        raise LLMError("Failed to generate SQL") from e
