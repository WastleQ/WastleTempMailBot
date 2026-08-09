# 🔐 WastleTempMailBot

Anonymous temporary email bot for Telegram (15 minutes lifespan), built as part of the **Wastle** ecosystem.

## Features
* 🌐 **Bilingual:** Russian and English support (`/start` language selection).
* ✉️ **Temp Mail:** Generate temporary email addresses instantly using Mail.tm API.
* 📬 **Inbox Management:** Check incoming verification codes and messages in real-time.
* 🛡 **Proxy Support:** Seamless integration with SOCKS5 proxies for reliable connection.

## Tech Stack
* Python 3.11+ (Async/Await)
* aiogram 3
* SQLite + aiosqlite
* Mail.tm API
* Ruff & Pytest

## Setup & Running
1. Clone / open directory.
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   PROXY_URL=socks5://127.0.0.1:10808
   ```
4. Run the bot:
   ```bash
   python3 bot.py
   ```
