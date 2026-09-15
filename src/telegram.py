import requests
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(text)
        return
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text}, timeout=20).raise_for_status()
