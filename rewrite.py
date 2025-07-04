import os
from together import Together
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=API_KEY)

def is_duplicate(title, link, log_file="logs/log.txt"):
    if not os.path.exists(log_file):
        return False
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if title in line or link in line:
                return True
    return False

def log_post(title, link, log_file="logs/log.txt"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().date()} | {title} | {link}\n")

def generate_post(title, summary, link, model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
    if is_duplicate(title, link):
        print(f"⚠️ Пост уже был: {title}")
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
- В конце — **практическая польза**
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    log_post(title, link)
    return content


# Пример запуска
if __name__ == "__main__":
    post = generate_post(
        title="AI discovers Earth-like planet",
        summary="An AI system detected a planet with similar atmospheric conditions as Earth.",
        link="https://example.com/earth-like-planet"
    )
    if post:
        print("\n📝 Сгенерированный пост:\n")
        print(post)
