import os
import time
import feedparser
from rewrite import generate_post
from datetime import datetime

POSTS_DIR = "posts"
os.makedirs(POSTS_DIR, exist_ok=True)

def read_rss_sources(file_path="rss_sources.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_news_from_rss(url, limit=3):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", "")
        })
    return items

def save_post(post_text, index):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}_{index:02}.txt"
    path = os.path.join(POSTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(post_text.strip())
    print(f"✅ Сохранено: {filename}")

if __name__ == "__main__":
    sources = read_rss_sources()
    all_news = []
    for url in sources:
        all_news.extend(fetch_news_from_rss(url, limit=3))

    print(f"🔍 Обнаружено {len(all_news)} новостей. Генерация...")

    for i, item in enumerate(all_news, start=1):
        print(f"\n#{i}: {item['title']}")
        post = generate_post(item["title"], item["summary"], item["link"])
        if post:
            save_post(post, i)
        else:
            print("❌ Не удалось сгенерировать пост.")
        time.sleep(2)
