import feedparser

def read_rss_sources(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_news_from_rss(url):
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:5]:  # первые 5 новостей с каждого источника
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary if "summary" in entry else "",
        })
    return news_items

if __name__ == "__main__":
    rss_urls = read_rss_sources("rss_sources.txt")
    all_news = []

    for url in rss_urls:
        print(f"\n🔗 Источник: {url}")
        news = fetch_news_from_rss(url)
        for item in news:
            print(f"— {item['title']}")
            print(f"  {item['link']}")
