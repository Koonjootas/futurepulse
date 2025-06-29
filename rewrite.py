import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://github.com/Koonjootas/futurepulse",
    "Content-Type": "application/json"
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

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print("❌ Сетевая ошибка:", e)
    except KeyError:
        print("❌ Ошибка: Не удалось извлечь результат из ответа.")
        print("Ответ сервера:", response.text)
    except Exception as e:
        print("❌ Непредвиденная ошибка:", e)

    return None

# Пример использования
if __name__ == "__main__":
    title = "AI Is Now Writing Its Own Research Papers"
    summary = "Artificial intelligence is being used to generate scientific papers with minimal human input. This trend raises questions about authorship and accuracy."
    post = generate_post(title, summary)
    print("\n📝 Сгенерированный пост:\n")
    print(post)
