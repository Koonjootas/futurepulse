import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Koonjootas/futurepulse",  # или твой сайт
    "X-Title": "FuturePulse"
}

def generate_post(title, summary, model="deepseek/deepseek-chat-v3-0324:free"):
    prompt = f"""
Ты пишешь посты для Telegram-канала @FuturePulse — ежедневно один научный инсайт.

Исходные данные:
Заголовок: {title}
Описание: {summary}

Сформируй пост:
— Цепляющий заголовок
— Краткое объяснение (1–2 абзаца)
— Максимум 500 символов
— Заверши вопросом или эмоцией
"""

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        data=json.dumps(payload)  # <-- именно data, а не json=
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("❌ Ошибка:", response.status_code, response.text)
        return None
