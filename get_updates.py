import requests

TOKEN = "7820604514:AAF2XONCtz8E7Vh8KRamC2QlLrd-P3FxsX8"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
r = requests.get(url)
print(r.json())
