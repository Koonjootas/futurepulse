import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка токена и ID из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DRAFT_CHAT_ID = os.getenv("DRAFT_CHAT_ID")           # Пример: -1002850405883
MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")       # Пример: @FuturePulse

# Посты будут отправляться из папки posts/
POSTS_DIR = "posts"
SENT_LOG = "sent_posts.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Загружаем отправленные посты
if os.path.exists(SENT_LOG):
    with open(SENT_LOG, "r", encoding="utf-8") as f:
        sent_files = set(json.load(f))
else:
    sent_files = set()

# Создание кнопок
def build_keyboard(filename):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Опубликовать", callback_data=f"publish|{filename}"),
         InlineKeyboardButton("🗑 Удалить", callback_data=f"delete|{filename}")]
    ])

# Команда для запуска выгрузки всех неотправленных постов
@dp.message_handler(commands=["send_posts"])
async def send_posts(message: types.Message):
    files = sorted(os.listdir(POSTS_DIR))
    new_files = [f for f in files if f not in sent_files and f.endswith(".txt")]

    if not new_files:
        await message.reply("Все посты уже отправлены.")
        return

    for filename in new_files:
        path = os.path.join(POSTS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        msg = await bot.send_message(
            chat_id=DRAFT_CHAT_ID,
            text=content,
            reply_markup=build_keyboard(filename),
            parse_mode="Markdown"
        )
        sent_files.add(filename)
        logging.info(f"Отправлен: {filename}")

    # Обновляем лог
    with open(SENT_LOG, "w", encoding="utf-8") as f:
        json.dump(list(sent_files), f)

# Обработка нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data.startswith("publish") or c.data.startswith("delete"))
async def handle_action(callback: types.CallbackQuery):
    action, filename = callback.data.split("|")
    path = os.path.join(POSTS_DIR, filename)

    if action == "publish":
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        await bot.send_message(chat_id=MAIN_CHANNEL_ID, text=content, parse_mode="Markdown")
        await callback.message.edit_text(f"✅ Опубликовано:\n\n{content}")
        logging.info(f"✅ Опубликовано: {filename}")

    elif action == "delete":
        if os.path.exists(path):
            os.remove(path)
        await callback.message.edit_text(f"🗑 Удалено: {filename}")
        logging.info(f"🗑 Удалено: {filename}")

    await callback.answer()

# Старт
if __name__ == "__main__":
    print("🚀 Бот запущен. Напиши /send_posts чтобы начать.")
    executor.start_polling(dp, skip_updates=True)
