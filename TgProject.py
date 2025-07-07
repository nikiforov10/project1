import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import random
from dotenv import load_dotenv
import os
load_dotenv()  # Загружает переменные из .env
TOKEN = os.getenv('TOKEN')

# === Настройки ===

TZ = "Europe/Moscow"  # Часовой пояс

# === Категории ===
CATEGORIES = {
    "birthday": {"emoji": "🎂", "style": "celebrate"},
    "workout": {"emoji": "💪", "style": "motivation"},
    "study": {"emoji": "📚", "style": "focus"},
}

# === Гифки ===
SUCCESS_GIFS = ["https://media.giphy.com/media/1.gif ", "https://media.giphy.com/media/2.gif "]
FAIL_GIFS = ["https://media.giphy.com/media/3.gif ", "https://media.giphy.com/media/4.gif "]

# === Хранилище в памяти ===
reminders = {}  # {user_id: [ {time, text, category, friend_id}, ... ]}
stats = {}  # {user_id: {total: 0, completed: 0}}

# === Инициализация бота ===
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ)

# === Команды ===
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in reminders:
        reminders[user_id] = []
        stats[user_id] = {"total": 0, "completed": 0}
    await message.reply("Привет! Добавьте напоминание:\n`15:00 Выпить воды workout`", parse_mode="Markdown")

@dp.message(Command("add"))
async def add_reminder(message: types.Message):
    await message.reply("Введите напоминание:\n`15:00 Выпить воды workout`", parse_mode="Markdown")

@dp.message(Command("stats"))
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    data = stats.get(user_id, {"total": 0, "completed": 0})
    percent = (data["completed"] / data["total"] * 100) if data["total"] else 0
    await message.reply(f"📊 Выполнено: {data['completed']}/{data['total']} ({percent:.1f}%)")

@dp.message(Command("help"))
async def help(message: types.Message):
    await message.reply("Доступные команды:\n/add\n/stats\n/help")

# === Обработка текстовых сообщений ===
@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    try:
        time_str, *rest = text.split()
        hour, minute = map(int, time_str.split(":"))
        category = rest[-1] if rest[-1] in CATEGORIES else None
        if category:
            text_content = " ".join(rest[:-1])
        else:
            text_content = " ".join(rest)
            category = "default"

        # Сохранение в словарь
        if user_id not in reminders:
            reminders[user_id] = []
        reminders[user_id].append({
            "time": time_str,
            "text": text_content,
            "category": category,
            "friend_id": None,  # Для парных напоминаний
        })

        # Добавление в планировщик
        scheduler.add_job(
            send_reminder,
            "cron",
            hour=hour,
            minute=minute,
            args=[user_id, text_content, category]
        )

        await message.reply(f"✅ Напоминание добавлено на {time_str}\nТекст: {text_content}")

    except Exception as e:
        await message.reply("❌ Неверный формат. Пример: `15:00 Выпить воды workout`", parse_mode="Markdown")

# === Отправка напоминаний ===
async def send_reminder(user_id, text, category):
    emoji = CATEGORIES.get(category, {}).get("emoji", "⏰")
    message = f"{emoji} {text}"
    try:
        await bot.send_message(user_id, message)
        await bot.send_animation(user_id, animation=random.choice(SUCCESS_GIFS))
    except Exception as e:
        print(f"Ошибка отправки пользователю {user_id}: {e}")

# === Запуск бота ===
async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())