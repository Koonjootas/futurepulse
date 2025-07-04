import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("DRAFT_CHAT_ID")  # или используй напрямую "@FuturePulse" для проверки

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "🔍 Тестовое сообщение от FuturePulse",
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    print("Status code:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    send_test_message()
