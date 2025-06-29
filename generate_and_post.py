import os
import json
import requests
import feedparser
from datetime import datetime
from dotenv import load_dotenv


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("DRAFT_CHAT_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://futurepulse.ai",
    "Content-Type": "application/json"
}

MODEL_ID = "deepseek-ai/deepseek-chat"  # бесплатная модель


def read_rss_sources(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_news_from_rss(url):
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:3]:  # первые 3 новости с источника
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary if "summary" in entry else "",
        })
    return news_items


def generate_post(title, summary, link):
    prompt = f"""
    Напиши пост в Telegram-канал на основе следующей новости:

    Заголовок: {title}
    Описание: {summary}
    Ссылка: {link}

    Задача:
    - Преврати это в короткий пост, до 500 символов
    - Заголовок должен быть вау-инсайтом, с практическим смыслом
    - Используй Markdown (жирный заголовок, абзацы)
    - Заверши вопросом к читателю
    """

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        print(f"Ошибка: {response.status_code} {response.text}")
        return None


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Telegram error: {response.text}")


def main():
    rss_urls = read_rss_sources("rss_sources.txt")
    all_news = []

    for url in rss_urls:
        all_news.extend(fetch_news_from_rss(url))

    for i, news in enumerate(all_news):
        post = generate_post(news["title"], news["summary"], news["link"])
        if post:
            send_to_telegram(post)


if __name__ == "__main__":
    main()
