import os
import time
import feedparser
from datetime import datetime
from rewrite import generate_post, is_duplicate

# Папка для сохранения сгенерированных постов
POSTS_DIR = "posts"
os.makedirs(POSTS_DIR, exist_ok=True)


def read_rss_sources(file_path="rss_sources.txt"):
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_news_from_rss(url, limit=3):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", "").strip(),
            "summary": entry.get("summary", "").strip()
        })
    return items


def save_post(post_text, link, index):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}_{index:02}.txt"
    path = os.path.join(POSTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(post_text.strip())
        f.write(f"\n\n🔗 Источник: {link}")
    print(f"✅ Сохранено: {filename}")


if __name__ == "__main__":
    sources = read_rss_sources()
    if not sources:
        print("⚠️ Нет RSS-источников.")
        exit()

    all_news = []
    for url in sources:
        all_news.extend(fetch_news_from_rss(url, limit=3))

    print(f"\n🔍 Обнаружено {len(all_news)} новостей. Генерация...\n")

    count = 0
    for i, item in enumerate(all_news, start=1):
        title, summary, link = item["title"], item["summary"], item["link"]

        if not title or not link:
            print(f"⚠️ Пропуск из-за пустого заголовка/ссылки #{i}")
            continue

        if is_duplicate(title, link):
            print(f"⏩ Дубликат: {title}")
            continue

        print(f"\n#{i}: {title}")
        post = generate_post(title, summary, link)
        if post:
            count += 1
            save_post(post, link, count)
        else:
            print("❌ Не удалось сгенерировать пост.")
        time.sleep(2)

    print(f"\n📦 Итог: {count} пост(ов) сохранено.")
