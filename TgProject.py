# from dotenv import load_dotenv
# import os
# load_dotenv()  # Загружает переменные из .env
# TOKEN = os.getenv('TOKEN')
# import asyncio
# import json
# import os
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from datetime import datetime, timedelta
# import pytz
# import random
#
# # === Настройки ===
# TZ = "Europe/Moscow"  # Часовой пояс
# DATA_FILE = "data.json"  # Файл для сохранения данных
#
# # === Категории ===
# CATEGORIES = {
#     "workout": {"emoji": "💪", "prefix": "Самое время на тренировку!"},
#     "birthday": {"emoji": "🎂", "prefix": "Сегодня день рождения у"},
#     "default": {"emoji": "⏰", "prefix": ""}
# }
#
# # === Гифки ===
# SUCCESS_GIFS = ["https://media.giphy.com/media/1.gif  ", "https://media.giphy.com/media/2.gif  "]
# FAIL_GIFS = ["https://media.giphy.com/media/3.gif  ", "https://media.giphy.com/media/4.gif  "]
#
# # === Хранилище в памяти ===
# reminders = {}  # {user_id: [ {time, date, text, category}, ... ]}
# stats = {}  # {user_id: {workout_count: 0, total_tasks: 0}}
# user_tags = {}  # {user_id: {tag_name: tag_text}}
# user_states = {}  # {user_id: state}
#
# # === Инициализация бота ===
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
# scheduler = AsyncIOScheduler(timezone=TZ)
#
# # === Главное меню ===
# main_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="🏋️ Статистика")],
#         [KeyboardButton(text="➕ Новое напоминание")],
#         [KeyboardButton(text="🏷️ Теги")],
#         [KeyboardButton(text="🔔 Мои уведомления")]
#     ],
#     resize_keyboard=True
# )
#
# # === Загрузка данных из файла ===
# def load_data():
#     global reminders, stats, user_tags
#     if os.path.exists(DATA_FILE):
#         try:
#             with open(DATA_FILE, "r") as f:
#                 data = json.load(f)
#                 reminders = {int(k): v for k, v in data.get("reminders", {}).items()}
#                 stats = {int(k): v for k, v in data.get("stats", {}).items()}
#                 user_tags = {int(k): v for k, v in data.get("user_tags", {}).items()}
#         except Exception as e:
#             print(f"Ошибка загрузки данных: {e}")
#
# # === Сохранение данных в файл ===
# def save_data():
#     try:
#         with open(DATA_FILE, "w") as f:
#             json.dump({
#                 "reminders": reminders,
#                 "stats": stats,
#                 "user_tags": user_tags
#             }, f, indent=2)
#     except Exception as e:
#         print(f"Ошибка сохранения данных: {e}")
#
# # === Команды ===
# @dp.message(Command("start"))
# async def start(message: types.Message):
#     user_id = message.from_user.id
#     if user_id not in reminders:
#         reminders[user_id] = []
#         stats[user_id] = {"workout_count": 0, "total_tasks": 0}
#         user_tags[user_id] = {}
#     await message.reply("Привет! Добавьте напоминание:\n`tag время текст`", parse_mode="Markdown",
#                         reply_markup=main_menu)
#
# @dp.message(lambda m: m.text == "🏋️ Статистика")
# @dp.message(Command("stats"))
# async def show_stats(message: types.Message):
#     user_id = message.from_user.id
#     data = stats.get(user_id, {"workout_count": 0, "total_tasks": 0})
#     await message.reply(f"🏋️ Тренировок выполнено: {data['workout_count']}\n"
#                         f"📊 Всего задач: {data['total_tasks']}")
#
# # === Управление тегами ===
# @dp.message(lambda m: m.text == "🏷️ Теги")
# @dp.message(Command("new_signal"))
# async def manage_tags(message: types.Message):
#     user_id = message.from_user.id
#     user_states[user_id] = "manage_tags"
#
#     # Формируем клавиатуру с тегами
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[])
#
#     # Системные теги
#     keyboard.inline_keyboard.append([
#         InlineKeyboardButton(text="📚 Системные теги", callback_data="system_tags")
#     ])
#     for tag in CATEGORIES:
#         if tag != "default":
#             keyboard.inline_keyboard.append([
#                 InlineKeyboardButton(text=f"🏷️ {tag}", callback_data=f"system_tag_{tag}")
#             ])
#
#     # Пользовательские теги
#     keyboard.inline_keyboard.append([
#         InlineKeyboardButton(text="🧩 Пользовательские теги", callback_data="user_tags")
#     ])
#     for tag in user_tags.get(user_id, {}):
#         keyboard.inline_keyboard.append([
#             InlineKeyboardButton(text=f"🏷️ {tag}", callback_data=f"edit_tag_{tag}")
#         ])
#
#     # Кнопка добавления нового тега
#     keyboard.inline_keyboard.append([
#         InlineKeyboardButton(text="➕ Новый тег", callback_data="add_tag")
#     ])
#
#     await message.reply("Управление тегами:\n\nВыберите тег для просмотра или создайте новый:", reply_markup=keyboard)
#
# # === Обработчики для тегов ===
# @dp.callback_query(lambda c: c.data == "add_tag")
# async def add_new_tag(callback: types.CallbackQuery):
#     user_id = callback.from_user.id
#     user_states[user_id] = "waiting_for_tag_name"
#     await callback.message.edit_text("Введите имя для нового тега:")
#
# @dp.callback_query(lambda c: c.data.startswith("edit_tag_"))
# async def edit_tag(callback: types.CallbackQuery):
#     user_id = callback.from_user.id
#     tag_name = callback.data.split("_")[2]
#     user_states[user_id] = f"editing_tag_{tag_name}"
#     current_text = user_tags[user_id].get(tag_name, "")
#     await callback.message.edit_text(f"Текущий текст для '{tag_name}': {current_text}\n\nВведите новый текст:")
#
# # === Обработка текстовых сообщений ===
# @dp.message()
# async def handle_text(message: types.Message):
#     user_id = message.from_user.id
#     text = message.text.strip()
#
#     # Обработка добавления тега
#     if user_states.get(user_id) == "waiting_for_tag_name":
#         user_states[user_id] = f"waiting_for_tag_text_{text}"
#         await message.reply(f"Введите текст для тега '{text}':")
#         return
#
#     elif user_states.get(user_id, "").startswith("waiting_for_tag_text_"):
#         tag_name = user_states[user_id].replace("waiting_for_tag_text_", "")
#         if user_id not in user_tags:
#             user_tags[user_id] = {}
#         user_tags[user_id][tag_name] = text
#         user_states.pop(user_id, None)
#         save_data()
#         await message.reply(f"✅ Тег '{tag_name}' создан!")
#         await manage_tags(message)
#         return
#
#     # Обработка редактирования тега
#     elif user_states.get(user_id, "").startswith("editing_tag_"):
#         tag_name = user_states[user_id].replace("editing_tag_", "")
#         user_tags[user_id][tag_name] = text
#         user_states.pop(user_id, None)
#         save_data()
#         await message.reply(f"✅ Тег '{tag_name}' обновлен!")
#         await manage_tags(message)
#         return
#
#     # Обработка добавления напоминания
#     if user_states.get(user_id) == "adding_reminder":
#         user_states.pop(user_id, None)
#         parts = text.split()
#         if not parts:
#             return
#
#         category = parts[0]
#         if category in CATEGORIES or category in user_tags.get(user_id, {}):
#             # Показываем доступные теги
#             system_tags = "\n".join([f"🏷️ {tag}" for tag in CATEGORIES if tag != "default"])
#             user_tag_list = user_tags.get(user_id, {})
#             user_tags_str = "\n".join([f"🏷️ {tag}" for tag in user_tag_list]) if user_tag_list else "Нет пользовательских тегов"
#
#             await message.reply(
#                 f"Доступные теги:\n"
#                 f"Системные:\n{system_tags}\n"
#                 f"Пользовательские:\n{user_tags_str}\n\n"
#                 f"Введите напоминание в формате:\n"
#                 f"[категория/тег] [время] [текст]\n"
#                 f"Пример:\n"
#                 f"{category} 15:00 Выпить воды"
#             )
#             return
#
#     # Парсинг категории и времени
#     parts = text.split()
#     if not parts:
#         return
#
#     # Если это команда создания напоминания
#     if parts[0] in CATEGORIES or parts[0] in user_tags.get(user_id, {}):
#         category = parts[0]
#         reminder_text = " ".join(parts[1:])  # Оставшийся текст
#
#         # Показываем доступные теги и примеры
#         system_tags = "\n".join([f"🏷️ {tag}" for tag in CATEGORIES if tag != "default"])
#         user_tag_list = user_tags.get(user_id, {})
#         user_tags_str = "\n".join([f"🏷️ {tag}" for tag in user_tag_list]) if user_tag_list else "Нет пользовательских тегов"
#
#         await message.reply(
#             f"Доступные теги:\n"
#             f"Системные:\n{system_tags}\n"
#             f"Пользовательские:\n{user_tags_str}\n\n"
#             f"Введите напоминание в формате:\n"
#             f"[категория/тег] [время] [текст]\n\n"
#             f"Пример для {category}:\n"
#             f"{category} 15:00 Выпить воды"
#         )
#         return
#
#     # Если это не команда управления тегами или напоминаниями
#     await message.reply("Неизвестная команда. Используйте главное меню.")
#
# # === Обработчики для уведомлений ===
# @dp.message(lambda m: m.text == "➕ Новое напоминание")
# async def new_reminder_prompt(message: types.Message):
#     user_id = message.from_user.id
#     user_states[user_id] = "adding_reminder"
#
#     # Формируем список доступных тегов
#     system_tags = "\n".join([f"🏷️ {tag}" for tag in CATEGORIES if tag != "default"])
#     user_tag_list = user_tags.get(user_id, {})
#     user_tags_str = "\n".join([f"🏷️ {tag}" for tag in user_tag_list]) if user_tag_list else "Нет пользовательских тегов"
#
#     await message.reply(
#         f"Введите напоминание в формате:\n"
#         f"[категория/тег] [время] [текст]\n\n"
#         f"Доступные теги:\n"
#         f"Системные:\n{system_tags}\n"
#         f"Пользовательские:\n{user_tags_str}",
#         parse_mode="Markdown"
#     )
#
# # === Отправка напоминаний ===
# async def send_reminder(user_id, text, category):
#     emoji = CATEGORIES.get(category, {}).get("emoji", "⏰")
#     prefix = CATEGORIES.get(category, {}).get("prefix", "")
#
#     # Проверка пользовательских тегов
#     if category in user_tags.get(user_id, {}):
#         prefix = ""
#         text = user_tags[user_id][category]
#
#     message = f"{emoji} {prefix} {text}" if prefix else f"{emoji} {text}"
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="✅ Выполнено", callback_data=f"complete_{user_id}_{category}_{text}")]
#     ])
#
#     try:
#         await bot.send_message(user_id, message, reply_markup=keyboard)
#         await bot.send_animation(user_id, animation=random.choice(SUCCESS_GIFS))
#     except Exception as e:
#         print(f"Ошибка отправки пользователю {user_id}: {e}")
#
# # === Обработчик нажатия на кнопку "Выполнено" ===
# @dp.callback_query()
# async def handle_complete(callback: types.CallbackQuery):
#     data = callback.data.split("_")
#     if data[0] == "complete":
#         user_id = int(data[1])
#         category = data[2]
#         text = "_".join(data[3:])  # Восстанавливаем текст, если был с пробелами
#
#         # Обновляем статистику только для тренировок
#         if category == "workout":
#             stats[user_id]["workout_count"] += 1
#         stats[user_id]["total_tasks"] += 1
#         save_data()
#
#         await callback.message.edit_text(f"✅ Вы успешно отметили выполнение: {text}")
#         await bot.send_animation(user_id, animation=random.choice(SUCCESS_GIFS))
#
# # === Обработчик удаления напоминаний ===
# @dp.message(lambda m: m.text == "🔔 Мои уведомления")
# @dp.message(Command("my_reminders"))
# async def my_reminders(message: types.Message):
#     user_id = message.from_user.id
#     user_reminders = reminders.get(user_id, [])
#
#     if not user_reminders:
#         await message.reply("У вас нет активных напоминаний.")
#         return
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[])
#     for idx, reminder in enumerate(user_reminders):
#         time_str = reminder.get("time", "")
#         text = reminder.get("text", "")
#         category = reminder.get("category", "")
#         date_str = reminder.get("date", "")
#
#         if category == "birthday" and date_str:
#             display = f"{CATEGORIES.get(category, {}).get('emoji', '⏰')} {date_str} {time_str} - {text}"
#         elif category in CATEGORIES:
#             display = f"{CATEGORIES.get(category, {}).get('emoji', '⏰')} {time_str} - {text}"
#         else:
#             display = f"⏰ {time_str} - {text}"
#
#         keyboard.inline_keyboard.append([
#             InlineKeyboardButton(text=display, callback_data=f"delete_reminder_{idx}")
#         ])
#
#     await message.reply("Ваши напоминания:", reply_markup=keyboard)
#
# @dp.callback_query()
# async def handle_delete_reminder(callback: types.CallbackQuery):
#     data = callback.data.split("_")
#     if data[0] == "delete":
#         user_id = callback.from_user.id
#         try:
#             idx = int(data[2])
#             if 0 <= idx < len(reminders.get(user_id, [])):
#                 removed = reminders[user_id].pop(idx)
#                 save_data()  # Сохраняем изменения
#                 await callback.message.edit_text(f"🗑 Удалено напоминание: {removed['text']}")
#         except (ValueError, IndexError):
#             pass
#
# # === Запуск бота ===
# async def main():
#     load_data()  # Загружаем данные при запуске
#
#     # Восстанавливаем планировщик
#     for user_id, user_reminders in reminders.items():
#         for reminder in user_reminders:
#             category = reminder.get("category")
#             time_str = reminder.get("time", "00:00")
#
#             try:
#                 hour, minute = map(int, time_str.split(":"))
#
#                 if category == "birthday":
#                     date_str = reminder.get("date", "01.01")
#                     day, month = map(int, date_str.split("."))
#                     scheduler.add_job(
#                         send_reminder,
#                         "cron",
#                         day=day,
#                         month=month,
#                         hour=hour,
#                         minute=minute,
#                         args=[user_id, reminder["text"], category]
#                     )
#                 else:
#                     scheduler.add_job(
#                         send_reminder,
#                         "cron",
#                         hour=hour,
#                         minute=minute,
#                         args=[user_id, reminder["text"], category]
#                     )
#             except Exception as e:
#                 print(f"Ошибка восстановления напоминания: {e}")
#
#     scheduler.start()
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     finally:
#         save_data()  # Сохраняем данные при завершении работы

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import random

# === Настройки ===
TZ = "Europe/Moscow"
DATA_FILE = "data.json"

# === Категории ===
CATEGORIES = {
    "workout": {"emoji": "💪", "prefix": "Самое время на тренировку!"},
    "birthday": {"emoji": "🎂", "prefix": "Сегодня день рождения у"},
    "default": {"emoji": "⏰", "prefix": ""}
}

# === Гифки ===
SUCCESS_GIFS = ["https://media.giphy.com/media/1.gif ", "https://media.giphy.com/media/2.gif "]
FAIL_GIFS = ["https://media.giphy.com/media/3.gif ", "https://media.giphy.com/media/4.gif "]

# === Хранилище ===
reminders = {}  # {user_id: [ {time, text, category}, ... ]}
stats = {}  # {user_id: {workout_count: 0, total_tasks: 0}}
user_tags = {}  # {user_id: {tag_name: tag_text}}
user_states = {}  # {user_id: state}

# === Инициализация бота ===
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ)

# === Главное меню ===
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🏋️ Статистика")],
    [KeyboardButton(text="➕ Новое напоминание")],
    [KeyboardButton(text="🏷️ Теги")],
    [KeyboardButton(text="🔔 Мои уведомления")]
], resize_keyboard=True)


# === Загрузка/сохранение данных ===
def load_data():
    global reminders, stats, user_tags
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                reminders = {int(k): v for k, v in data.get("reminders", {}).items()}
                stats = {int(k): v for k, v in data.get("stats", {}).items()}
                user_tags = {int(k): v for k, v in data.get("user_tags", {}).items()}
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")


def save_data():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({
                "reminders": reminders,
                "stats": stats,
                "user_tags": user_tags
            }, f, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")


# === Обработчики команд ===
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in reminders:
        reminders[user_id] = []
        stats[user_id] = {"workout_count": 0, "total_tasks": 0}
        user_tags[user_id] = {}
    await message.reply("Привет! Добавьте напоминание:\n`tag время текст`",
                        parse_mode="Markdown", reply_markup=main_menu)


@dp.message(lambda m: m.text == "🏋️ Статистика")
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    data = stats.get(user_id, {"workout_count": 0, "total_tasks": 0})
    await message.reply(f"🏋️ Тренировок выполнено: {data['workout_count']}\n"
                        f"📊 Всего задач: {data['total_tasks']}")


# === Управление тегами ===
@dp.message(lambda m: m.text == "🏷️ Теги")
async def manage_tags(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = "manage_tags"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for tag in user_tags.get(user_id, {}):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=f"🏷️ {tag}", callback_data=f"edit_tag_{tag}")
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="➕ Новый тег", callback_data="add_tag")
    ])
    await message.reply("Выберите тег для редактирования или создайте новый:", reply_markup=keyboard)


# === Новое напоминание ===
@dp.message(lambda m: m.text == "➕ Новое напоминание")
async def new_reminder_prompt(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = "adding_reminder"

    system_tags = "\n".join([f"🏷️ {tag}" for tag in CATEGORIES if tag != "default"])
    user_tags_str = "\n".join([f"🏷️ {tag}" for tag in user_tags.get(user_id, {})]) or "Нет пользовательских тегов"

    await message.reply(
        f"Введите напоминание в формате:\n"
        f"[категория/тег] [время] [текст]\n\n"
        f"Доступные теги:\n"
        f"Системные:\n{system_tags}\n"
        f"Пользовательские:\n{user_tags_str}",
        parse_mode="Markdown"
    )


# === Мои уведомления ===
@dp.message(lambda m: m.text == "🔔 Мои уведомления")
async def show_my_reminders(message: types.Message):
    user_id = message.from_user.id
    user_reminders = reminders.get(user_id, [])

    if not user_reminders:
        await message.reply("У вас нет активных напоминаний.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for idx, reminder in enumerate(user_reminders):
        time_str = reminder.get("time", "")
        text = reminder.get("text", "")
        category = reminder.get("category", "")

        display = f"{CATEGORIES.get(category, {}).get('emoji', '⏰')} {time_str} - {text}"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=display, callback_data=f"delete_reminder_{idx}")
        ])

    await message.reply("Ваши напоминания - нажмите чтобы удалить:", reply_markup=keyboard)


# === Обработка текстовых сообщений ===
@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip().lower()

    # Исключаем известные команды
    if text in ["🏋️ статистика", "🔔 мои уведомления", "➕ новое напоминание", "🏷️ теги"]:
        return

    # Обработка добавления тега
    if user_states.get(user_id) == "waiting_for_tag_name":
        user_states[user_id] = "waiting_for_tag_text"
        user_states[f"{user_id}_temp_tag"] = text
        await message.reply("Введите текст для этого тега:")
        return

    elif user_states.get(user_id) == "waiting_for_tag_text":
        tag_name = user_states.get(f"{user_id}_temp_tag")
        if tag_name:
            if user_id not in user_tags:
                user_tags[user_id] = {}
            user_tags[user_id][tag_name] = text
            user_states.pop(f"{user_id}_temp_tag", None)
            user_states.pop(user_id, None)
            save_data()
            await message.reply(f"✅ Тег '{tag_name}' создан!")
            await manage_tags(message)
        return

    # Обработка добавления напоминания
    if user_states.get(user_id) == "adding_reminder":
        parts = text.split()
        if len(parts) < 3:
            await message.reply("❌ Неверный формат. Пример: workout 15:00 Выпить воды")
            return

        category = parts[0]
        time_str = parts[1]
        reminder_text = " ".join(parts[2:])

        try:
            hour, minute = map(int, time_str.split(":"))

            if user_id not in reminders:
                reminders[user_id] = []

            reminders[user_id].append({
                "time": time_str,
                "text": reminder_text,
                "category": category
            })
            save_data()

            scheduler.add_job(
                send_reminder,
                "cron",
                hour=hour,
                minute=minute,
                args=[user_id, reminder_text, category]
            )
            await message.reply(f"✅ Напоминание добавлено: {reminder_text}")
            user_states.pop(user_id, None)

        except (ValueError, IndexError):
            await message.reply("❌ Неверный формат времени. Пример: 15:00")
        return


# === Отправка напоминаний ===
async def send_reminder(user_id, text, category):
    emoji = CATEGORIES.get(category, {}).get("emoji", "⏰")
    prefix = CATEGORIES.get(category, {}).get("prefix", "")

    if category in user_tags.get(user_id, {}):
        prefix = ""
        text = user_tags[user_id][category]

    message = f"{emoji} {prefix} {text}" if prefix else f"{emoji} {text}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Выполнено",
            callback_data=f"complete_{user_id}_{category}_{text.replace(' ', '_')}"
        )]
    ])

    try:
        await bot.send_message(user_id, message, reply_markup=keyboard)
        await bot.send_animation(user_id, animation=random.choice(SUCCESS_GIFS))
    except Exception as e:
        print(f"Ошибка отправки пользователю {user_id}: {e}")


# === Обработчики callback ===
@dp.callback_query(lambda c: c.data.startswith("delete_reminder_"))
async def handle_delete_reminder(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        idx = int(callback.data.split("_")[2])

        if 0 <= idx < len(reminders.get(user_id, [])):
            removed = reminders[user_id].pop(idx)
            save_data()
            await callback.message.edit_text(f"🗑 Удалено напоминание: {removed['text']}")
        else:
            await callback.answer("❌ Напоминание не найдено")

    except (ValueError, IndexError) as e:
        print(f"Ошибка удаления: {e}")
        await callback.answer("❌ Ошибка удаления напоминания")


@dp.callback_query(lambda c: c.data.startswith("add_tag"))
async def handle_add_tag(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = "waiting_for_tag_name"
    await callback.message.edit_text("Введите имя для нового тега:")


@dp.callback_query(lambda c: c.data.startswith("edit_tag_"))
async def handle_edit_tag(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tag_name = callback.data.split("_")[2]
    user_states[user_id] = f"editing_tag_{tag_name}"
    current_text = user_tags[user_id].get(tag_name, "")
    await callback.message.edit_text(f"Текст для '{tag_name}': {current_text}\n\nВведите новый текст:")


# === Обработчик выполнения задачи ===
@dp.callback_query(lambda c: c.data.startswith("complete_"))
async def handle_complete(callback: types.CallbackQuery):
    try:
        # Разбираем callback_data на части (максимум 4 части)
        parts = callback.data.split("_", 3)  # ["complete", user_id, category, text]

        if len(parts) < 4:
            await callback.answer("❌ Неверный формат данных")
            return

        _, user_id_str, category, text = parts

        # Преобразуем user_id в int
        try:
            user_id = int(user_id_str)
        except ValueError:
            await callback.answer("❌ Ошибка: неверный ID пользователя")
            return

        # Обновляем статистику
        if user_id not in stats:
            stats[user_id] = {"workout_count": 0, "total_tasks": 0}

        if category == "workout":
            stats[user_id]["workout_count"] = stats[user_id].get("workout_count", 0) + 1
        stats[user_id]["total_tasks"] = stats[user_id].get("total_tasks", 0) + 1
        save_data()  # Сохраняем обновления

        # Подтверждаем выполнение
        await callback.message.edit_text(f"✅ Вы успешно отметили выполнение: {text}")
        await bot.send_animation(callback.from_user.id, animation=random.choice(SUCCESS_GIFS))

    except Exception as e:
        print(f"Ошибка при обработке выполнения: {e}")
        await callback.answer("❌ Произошла ошибка при обработке выполнения")


# === Запуск бота ===
async def main():
    load_data()

    for user_id, user_reminders in reminders.items():
        for reminder in user_reminders:
            try:
                category = reminder.get("category")
                time_str = reminder.get("time", "00:00")
                hour, minute = map(int, time_str.split(":"))

                scheduler.add_job(
                    send_reminder,
                    "cron",
                    hour=hour,
                    minute=minute,
                    args=[user_id, reminder["text"], category]
                )
            except Exception as e:
                print(f"Ошибка восстановления напоминания: {e}")

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        save_data()