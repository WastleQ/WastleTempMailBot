import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database.db"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MAIL_API_BASE = os.getenv("MAIL_API_BASE", "https://api.mail.tm")
PROXY_URL = os.getenv("PROXY_URL", "")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "8080"))
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8080")
