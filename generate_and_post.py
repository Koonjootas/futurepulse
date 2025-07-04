from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("DRAFT_CHAT_ID")
FOLDER = "posts"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("❌ Ошибка отправки:", response.status_code, response.text)
    else:
        print("✅ Отправлено:", text[:40], "...")

def main():
    print("📁 Текущая директория:", os.getcwd())
    if not os.path.exists(FOLDER):
        print(f"❌ Папка '{FOLDER}' не найдена")
        return

    all_files = os.listdir(FOLDER)
    print(f"📄 Найдено файлов: {len(all_files)} →", all_files)

    files = sorted(
        f for f in all_files
        if f.lower().endswith(".txt") and f[:10].replace("-", "").isdigit()
    )

    if not files:
        print(f"⚠️ Нет подходящих файлов для обработки в папке '{FOLDER}'")
        return

    for filename in files:
        filepath = os.path.join(FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                print(f"📤 Отправка: {filename}")
                send_to_telegram(content)
            else:
                print(f"⚠️ Пустой файл: {filename}")

if __name__ == "__main__":
    main()
