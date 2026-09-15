from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
SYMBOL = '^NSEBANK'
MARKET_TZ = 'Asia/Kolkata'
MIN_SCORE = 75
DATA_DIR = ROOT / 'data'
JOURNAL = DATA_DIR / 'trade_journal.json'
