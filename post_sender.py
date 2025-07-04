import os
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("DRAFT_CHAT_ID")

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("❌ Ошибка отправки:", response.status_code, response.text)
    else:
        print("✅ Отправлено:", text[:40], "...")
