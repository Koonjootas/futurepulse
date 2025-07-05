import os
from together import Together
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=API_KEY)

LOG_FILE = "logs/log.txt"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()


def is_duplicate(title, link, log_file=LOG_FILE):
    if not os.path.exists(log_file):
        return False
    with open(log_file, "r", encoding="utf-8") as f:
        return any(title in line or link in line for line in f.readlines())


def log_post(title, link, log_file=LOG_FILE):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {title.strip()} | {link.strip()}\n")


def generate_post(title, summary, link, model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
    if not title or not summary or not link:
        print("❌ Ошибка: один из параметров пустой.")
        return None

    if is_duplicate(title, link):
        print(f"⚠️ Пропуск (дубликат): {title}")
        return None

    prompt = f"""
Ты пишешь посты для Telegram-канала @FuturePulse — ежедневно один научный инсайт.

Tone of Voice:
- Пишешь как умный, но не занудный собеседник.
- Инсайт — главное: удивляй, но не кликбей.
- Без воды и сложных терминов — максимум сути, минимум лишнего.
- Каждый пост должен быть как разговор с любознательным другом, который вдохновляет, а не поучает.
- Будь футуристичным, но сдержанным. Без "учёные в шоке" — только реальные WOW-факты.

Исходные данные:
**Заголовок:** {title}
**Описание:** {summary}
**Ссылка:** {link}

Сформируй пост:
- **Цепляющий заголовок** (выдели жирным через `**`)
- 2–4 абзаца с объяснением — пиши как будто рассказываешь другу, которому интересно
- Избегай штампов и клише. Пиши коротко, но образно
- До 600 символов
- Используй Markdown для форматирования
- В конце добавь ненавязчивую практическую пользу
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        if content:
            log_post(title, link)
            return content
        else:
            print("❌ Ответ от модели пуст.")
            return None

    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return None


# Пример для локального теста
if __name__ == "__main__":
    test_post = generate_post(
        title="AI discovers Earth-like planet",
        summary="An AI system detected a planet with similar atmospheric conditions as Earth.",
        link="https://example.com/earth-like-planet"
    )
    if test_post:
        print("\n📝 Сгенерированный пост:\n")
        print(test_post)
