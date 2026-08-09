# WastleTempMailBot - Agent Instructions & Architecture

## Project Overview
Telegram bot providing anonymous temporary email addresses (15 min lifespan) with bilingual support (RU/EN) as part of the Wastle ecosystem.

## Technical Stack
* **Language:** Python 3.11+ (Async/Await)
* **Framework:** aiogram 3
* **Database:** SQLite + aiosqlite
* **Mail Backend:** Mail.tm API
* **Linter/Formatter:** ruff

## Key Features
1. **Bilingual:** Choice of Russian or English on `/start`.
2. **Temp Mail Generation:** Generate email via Mail.tm API, with 15-minute countdown/lifespan.
3. **Inbox Checking:** Fetch incoming messages (verification codes, links).
4. **Ecosystem Branding:** Wastle branding across all messages and prompts.
