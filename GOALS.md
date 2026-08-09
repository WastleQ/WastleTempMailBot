# 🎯 GOALS.md - WastleTempMailBot Roadmap

## 📌 Stage 1: Smart Email Parsing (HTML, Verification Codes & Links) - COMPLETED
* [x] Basic temp email generation and inbox listing.
* [x] Fetch full message details (`GET /messages/{id}`).
* [x] Parse HTML body to plain text.
* [x] Use Regex to extract verification codes (4-6 digits).
* [x] Extract verification/activation links.

## 🚀 Stage 2: Telegram Mini App (TMA) - COMPLETED
* [x] Create frontend web interface (`webapp/index.html`) representing a full webmail client with Tailwind CSS and Telegram WebApp SDK.
* [x] Build backend API endpoints (`webapp_api.py`) to bridge TMA with Mail.tm API and database.
* [x] Implement active mailbox, email list, message viewer, and copy buttons.
* [x] Integrate WebApp button in the main chat bot keyboard.

## 🌐 Stage 3: Custom Domain Integration (Future)
* [ ] Purchase custom domain.
* [ ] Configure DNS records and Mail.tm custom domain API.
* [ ] Offer exclusive Wastle domain email addresses to users.
