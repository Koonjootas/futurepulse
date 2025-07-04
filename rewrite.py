import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Koonjootas/futurepulse",  # замените, если нужно
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

    for attempt in range(3):  # до 3 попыток
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=HEADERS,
                json=payload,
                timeout=60  # явный таймаут
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"❌ Попытка {attempt + 1}: HTTP {response.status_code}: {response.text}")
                break  # не повторяем, если ошибка на уровне API
        except requests.exceptions.ChunkedEncodingError as e:
            print(f"⚠️ Попытка {attempt + 1}: ChunkedEncodingError — {e}. Повтор через 5 сек...")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Попытка {attempt + 1}: Другая ошибка — {e}. Повтор через 5 сек...")
            time.sleep(5)
    return None


# Пример теста
if __name__ == "__main__":
    title = "AI Is Now Writing Its Own Research Papers"
    summary = "Artificial intelligence is being used to generate scientific papers with minimal human input. This trend raises questions about authorship and accuracy."
    post = generate_post(title, summary)
    print("\n📝 Сгенерированный пост:\n")
    print(post)
