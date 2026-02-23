# Video Analytics Bot

Telegram-бот для анализа статистики видео. Принимает вопросы на естественном языке, преобразует их в SQL-запросы с помощью LLM и возвращает результат из базы данных.

---

## Запуск проекта

**1. Клонировать репозиторий**

```bash
git clone git@github.com:EcLerk/video-analytics-bot.git
cd video-analytics-bot
```

**2. Создать `.env` файл на основе примера**

```bash
cp .env.example .env
```

Заполнить переменные (см. раздел ниже).

**3. Запустить контейнеры**

```bash
docker compose up --build
```

**4. Загрузить данные из JSON в базу**

```bash
make load-data
```

или без make:

```bash
docker compose exec bot python -m scripts.load_data
```

---

## Переменные окружения

Все переменные задаются в файле `.env` в корне проекта:

```env
# База данных
DATABASE__USER=user
DATABASE__PASSWORD=pass
DATABASE__NAME=db-name

# Telegram
TG__API_KEY=your-telegram-api-key

# LLM (Gemini)
OPENAI__API_KEY=your-gemini-api-key
```

### Как получить токен Telegram-бота

1. Открыть Telegram и найти `@BotFather`
2. Написать `/newbot`
3. Указать название и username бота (username должен заканчиваться на `bot`)
4. Скопировать выданный токен и вставить в `TG__API_KEY`

### Как получить API-ключ Gemini

1. Зайти на [aistudio.google.com](https://aistudio.google.com)
2. Перейти в `API keys` → `Create API key`
3. Скопировать ключ и вставить в `OPENAI__API_KEY`

---

## Архитектура проекта

```
src/
  app/
    bot/              # Telegram-хэндлеры (aiogram)
    config/           # Настройки через pydantic-settings
    db/               # SQLAlchemy модели, engine, session
    services/              # Генерация SQL через LLM + выполнение запросов
    schemas/          # Pydantic/dataclass схемы для парсинга JSON
    /exceptions     # Кастомные исключения
  scripts/
    load_data.py      # Скрипт импорта данных из JSON
  main.py
```

**Стек:** Python 3.12, aiogram 3, SQLAlchemy 2 (async), PostgreSQL, Gemini API (совместим с OpenAI SDK), Docker.

---

## Подход к преобразованию текста в SQL

Пользователь пишет вопрос на русском языке → бот отправляет его в Gemini вместе с системным промптом, описывающим схему БД → модель возвращает SQL-запрос → бот выполняет запрос и отвращает результат.

### Схема данных в промпте

Модели описаны текстом с указанием типов, назначения каждого поля и правил выборки:

```
Таблица videos — текущее состояние видео:
- id (UUID) — уникальный идентификатор
- creator_id (str) — идентификатор автора
- video_created_at (timestamptz) — дата публикации
- views_count, likes_count, comments_count, reports_count (int) — текущие метрики

Таблица snapshots — исторические срезы метрик:
- video_id (UUID) — ссылка на videos.id
- views_count, likes_count, comments_count, reports_count (int) — метрики на момент снапшота
- delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count (int) — прирост с предыдущего снапшота
- created_at (timestamptz) — дата создания снапшота

Правила:
- Текущие метрики → таблица videos
- Исторические данные и приросты → таблица snapshots
```

### Системный промпт

Промпт содержит описание схемы и жёсткие ограничения для модели:

- возвращать только SQL без пояснений и markdown
- использовать только `SELECT`
- возвращать только одно число

`temperature=0` гарантирует детерминированные ответы — для одного и того же вопроса модель всегда вернёт одинаковый SQL.

### Защита от небезопасных запросов

Перед выполнением каждый SQL проходит валидацию — проверяется что запрос начинается с `SELECT` и не содержит `INSERT`, `UPDATE`, `DELETE`, `DROP` и других модифицирующих операторов.
