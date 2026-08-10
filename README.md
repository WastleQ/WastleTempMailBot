# 🔐 WastleTempMailBot

**WastleTempMailBot** is an enterprise-grade, high-performance Telegram Bot and Telegram Mini App (TMA) built as a core service of the **Wastle Ecosystem**. It provides secure, anonymous, temporary email addresses with real-time push notifications and live webmail synchronization.

---

## 🏗 Architectural Overview

The application features a **Dual-Stack Concurrent Architecture** running on a single Python async event loop (`asyncio`):
1. **Telegram Bot Core (`aiogram 3`):** Asynchronous long-polling interface supporting bilingual localization (RU/EN), interactive keyboards, and chat commands (`/start`, `/status`, `/webapp`).
2. **Web Application Server (`aiohttp`):** Embedded web server serving the Telegram Mini App (TMA) and REST/SSE API endpoints concurrently with the bot.
3. **Real-Time Event Streaming (SSE):** Server-Sent Events (`/api/stream/{user_id}`) stream instant inbox updates to the frontend without heavy polling overhead.
4. **Resilient Network Layer:** Built-in SOCKS5 proxy support via `aiohttp-socks` ensuring robust connectivity across restricted networks.

---

## ✨ Key Features

* 🌐 **Bilingual Localization:** Full Russian and English support with persistent user preference storage.
* ⚡ **Real-Time Push Notifications:** Background worker (`mail_watcher_worker`) polls active mailboxes every 15 seconds and pushes instant notifications to the user's Telegram chat upon receiving new emails.
* 📱 **Telegram Mini App (TMA):** Modern dark-mode mobile-first web interface built with Tailwind CSS and Telegram WebApp SDK, featuring live 15-minute UTC countdown timers and one-click copy.
* 🛡 **Secure Mail Backend:** Powered by the Mail.tm API with zero local email server overhead.
* ⚙️ **Dynamic Schema Migrations:** SQLite database with automated zero-downtime schema checks via `PRAGMA table_info`.

---

## 🛠 Tech Stack

* **Language:** Python 3.11+ (Strict Async/Await)
* **Bot Framework:** `aiogram 3.3.0+`
* **Web & API:** `aiohttp`, Server-Sent Events (SSE)
* **Database:** SQLite + `aiosqlite`
* **Code Quality & Testing:** `ruff`, `pytest`, `pytest-asyncio`

---

## 📂 Project Structure

```text
WastleTempMailBot/
├── bot.py             # Main entry point: aiogram dispatcher + concurrent aiohttp server & watcher worker
├── webapp_api.py      # TMA REST API and SSE real-time event streaming endpoints
├── mail_api.py        # Mail.tm API client with SOCKS5 proxy support
├── email_parser.py    # HTML-to-text sanitization utilities
├── database.py        # Asynchronous SQLite storage & dynamic migrations
├── keyboards.py       # Dynamic Telegram Reply Keyboards & WebApp buttons
├── locales.py         # Bilingual localization dictionaries (RU/EN)
├── webapp/            # Telegram Mini App frontend (Tailwind CSS + WebApp SDK)
├── test_bot.py        # Pytest unit test suite
├── requirements.txt   # Python dependencies
└── .env               # Environment configuration
```

---

## 🚀 Setup & Deployment

### 1. Local Development
1. Clone the repository and navigate to the project folder.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure your `.env` file:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   PROXY_URL=socks5://127.0.0.1:10808   # Optional: SOCKS5 proxy
   WEBAPP_URL=http://localhost:8080
   ```
4. Run the application:
   ```bash
   python3 bot.py
   ```

### 2. Production Deployment (Render.com)
The project is fully prepared for zero-downtime deployment on Render:
* **Runtime:** Python 3
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `python3 bot.py`
* **Environment Variables:** `BOT_TOKEN`, `WEBAPP_URL` (`https://your-service.onrender.com`), and automated `PORT`.
