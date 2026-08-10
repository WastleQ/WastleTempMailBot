# Development Log - WastleTempMailBot

## [1.6.0] - 2026-08-06 (Live Bidirectional Sync)
* Implemented live bidirectional mailbox state sync in SSE stream (`/api/stream/{user_id}`).
* TMA frontend now auto-detects mailbox creation or deletion performed in Telegram Chat and updates UI instantly without page reload.
* Added `tg.ready()` in `webapp/index.html` to guarantee Telegram WebApp SDK initialization.
* Validated codebase and unit tests with Ruff and Pytest.

## [1.5.1] - 2026-08-06 (Timer & Strict Sync Fixes)
* Fixed UTC date parsing in `webapp/index.html` so the 15-minute countdown timer displays correctly instead of immediately expiring.
* Enforced strict priority on Telegram `user.id` (`tg.initDataUnsafe.user.id` and URL query params) in TMA to ensure 100% account synchronization between chat bot and Mini App.
* Validated codebase and unit tests with Ruff and Pytest.

## [1.5.0] - 2026-08-06 (Status Command & Delete Fixes)
* Added `/status` command (and keywords "статус", "status") to display the currently active email address.
* Verified that deleting a mailbox (`🗑 Удалить почту`) permanently clears the active mailbox without automatically generating a new one.
* Validated codebase and unit tests with Ruff and Pytest.

## [1.4.0] - 2026-08-06 (Render Production Deployment)
* Successfully deployed **WastleTempMailBot** and Telegram Mini App to Render.com (`https://wastletempmailbot.onrender.com`).
* Configured environment variables (`BOT_TOKEN`, `WEBAPP_URL`) on Render.
* Validated code quality and unit tests with Ruff and Pytest.

## [1.3.0] - 2026-08-06 (Pinggy Tunnel & Cleanup)
* Cleaned up redundant localtunnel helper scripts (`run_tunnel.sh`, `start_all.sh`).
* Integrated Pinggy SSH tunnel (`start_pinggy_all.sh`) with `-o PubkeyAuthentication=no` for seamless public HTTPS tunneling.
* Validated codebase with Ruff and Pytest; all checks passed successfully.

## [1.2.0] - 2026-08-06 (Stage 2: Telegram Mini App - TMA)
* Implemented Telegram Mini App (TMA) frontend in `webapp/index.html` using Tailwind CSS and Telegram WebApp SDK.
* Created backend API endpoints in `webapp_api.py` for user mailboxes, mailbox creation, and enriched message fetching with link extraction.
* Added WebApp launch button to the main Telegram bot keyboard (`get_main_keyboard`).
* Integrated aiohttp web server running concurrently with aiogram bot polling on `WEBAPP_PORT`.

## [1.1.0] - 2026-08-06 (Stage 1: Smart Email Parsing)
* Initiated development of Stage 1: Smart Email Parsing.
* Planned HTML body parsing, automatic 4-6 digit verification code extraction using Regex, and activation link extraction for modern registration forms (like AniLiberty).
* Set up GOALS.md roadmap for Stage 1 (Chat Bot parsing), Stage 2 (TMA), and Stage 3 (Custom Domain).

## [1.0.0] - 2026-08-06
* Initial release of **WastleTempMailBot** (part of the Wastle Ecosystem).
* Implemented bilingual support (Russian & English) with persistent user preference storage.
* Integrated Mail.tm API for asynchronous temporary email creation (15-minute lifespan) and inbox checking.
* Added SOCKS5 proxy support via `aiohttp-socks` to ensure stable connectivity in restricted network environments.
* Structured code following Python 3.11+ async standards, validated with Ruff and tested with Pytest.
