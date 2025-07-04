import os
from post_sender import send_to_telegram

POSTS_DIR = "posts"

def process_posts():
    if not os.path.exists(POSTS_DIR):
        print(f"⚠️ Папка '{POSTS_DIR}' не найдена.")
        return

    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".txt")]
    if not files:
        print(f"⚠️ Нет файлов для обработки в папке '{POSTS_DIR}'")
        return

    for file_name in files:
        file_path = os.path.join(POSTS_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            send_to_telegram(content)
        else:
            print(f"⚠️ Файл пустой: {file_name}")

        os.remove(file_path)

if __name__ == "__main__":
    process_posts()
