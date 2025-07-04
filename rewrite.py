import os
from together import Together
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=API_KEY)

def generate_post(title, summary, link, model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
    prompt = f"""
Ты пишешь посты для Telegram-канала @FuturePulse — ежедневно один научный инсайт.

Исходные данные:
**Заголовок:** {title}
**Описание:** {summary}
**Ссылка:** {link}

Сформируй пост:
- **Цепляющий заголовок** (жирный)
- 1–2 абзаца с кратким объяснением
- До 500 символов
- Используй Markdown
- Заверши вопросом или эмоцией
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Пример запуска
if __name__ == "__main__":
    post = generate_post(
        title="AI discovers Earth-like planet",
        summary="An AI system detected a planet with similar atmospheric conditions as Earth.",
        link="https://example.com/earth-like-planet"
    )
    print("\n📝 Сгенерированный пост:\n")
    print(post)
