import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web
from config import BOT_TOKEN, PROXY_URL, WEBAPP_PORT, WEBAPP_URL
from database import (
    clear_user_mailbox,
    get_all_active_users,
    get_user,
    init_db,
    set_user_language,
    set_user_mailbox,
)
from email_parser import clean_html_to_text
from keyboards import get_lang_keyboard, get_main_keyboard
from locales import get_text
from mail_api import create_temp_mail, get_message_detail, get_messages
from webapp_api import setup_webapp_routes

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "your_telegram_bot_token_here":
        print("ERROR: BOT_TOKEN is not set in environment or .env file!")
        return

    await init_db()

    session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else AiohttpSession()
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        if not user_data:
            # Ask for language
            await message.answer(
                "🌐 Please choose your language / Выберите язык:",
                reply_markup=get_lang_keyboard()
            )
        else:
            lang = user_data[0]
            await message.answer(
                get_text(lang, "welcome"),
                reply_markup=get_main_keyboard(lang),
                parse_mode="Markdown"
            )

    @dp.message(Command("webapp"))
    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["webapp", "веб-приложение"])))
    async def cmd_webapp(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        lang = user_data[0] if user_data else "ru"
        app_url = f"{WEBAPP_URL}?user_id={message.from_user.id}"
        if lang == "en":
            text = f"🌐 **WastleTempMail WebApp**:\n{app_url}\n\n*(Open the link above to view your synchronized mailbox).* "
        else:
            text = f"🌐 **Веб-приложение WastleTempMail**:\n{app_url}\n\n*(Откройте ссылку выше для доступа к вашей синхронизированной почте).* "
        await message.answer(text, parse_mode="Markdown")

    @dp.message(Command("status"))
    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["статус", "status"])))
    async def cmd_status(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        lang = user_data[0] if user_data else "ru"
        email = user_data[1] if user_data else None

        if not email:
            await message.answer(get_text(lang, "status_none"), reply_markup=get_main_keyboard(lang))
        else:
            await message.answer(
                get_text(lang, "status_active", email=email),
                reply_markup=get_main_keyboard(lang),
                parse_mode="Markdown"
            )

    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["русский", "english"])))
    async def lang_chosen(message: Message) -> None:
        lang = "ru" if "русский" in message.text.lower() else "en"
        await set_user_language(message.from_user.id, lang)
        await message.answer(
            get_text(lang, "lang_set"),
            reply_markup=get_main_keyboard(lang)
        )
        await message.answer(
            get_text(lang, "welcome"),
            reply_markup=get_main_keyboard(lang),
            parse_mode="Markdown"
        )

    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["сменить", "change", "язык", "language"])))
    async def change_lang(message: Message) -> None:
        await message.answer(
            "🌐 Please choose your language / Выберите язык:",
            reply_markup=get_lang_keyboard()
        )

    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["создать", "create", "✉️"]) and "удалить" not in t.lower() and "delete" not in t.lower()))
    async def create_mail(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        lang = user_data[0] if user_data else "ru"

        wait_msg = await message.answer("⏳ Создаем временный ящик..." if lang == "ru" else "⏳ Creating temporary mailbox...")
        
        result = await create_temp_mail()
        if not result:
            await wait_msg.edit_text("❌ Ошибка создания почты. Попробуйте позже." if lang == "ru" else "❌ Error creating mailbox. Try later.")
            return

        await set_user_mailbox(message.from_user.id, result["email"], result["mail_id"], result["token"])
        await wait_msg.edit_text(
            get_text(lang, "mail_created", email=result["email"]),
            parse_mode="Markdown"
        )

    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["проверить", "check", "входящие", "inbox"])))
    async def check_inbox(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        lang = user_data[0] if user_data else "ru"
        if not user_data or not user_data[1]:
            await message.answer(get_text(lang, "no_mail"), reply_markup=get_main_keyboard(lang))
            return

        _, _, _, token = user_data

        wait_msg = await message.answer("🔍 Проверяем почту..." if lang == "ru" else "🔍 Checking inbox...")
        messages = await get_messages(token)

        if not messages:
            await wait_msg.edit_text(get_text(lang, "inbox_empty"))
            return

        await wait_msg.delete()

        for msg in messages[:3]:
            msg_id = msg.get("id")
            detail = await get_message_detail(token, msg_id) if msg_id else None

            sender = msg.get("from", {}).get("address", "Unknown")
            subject = msg.get("subject", "No Subject")

            html_content = detail.get("html", "") if detail else ""
            text_content = detail.get("text", "") if detail else msg.get("intro", "")

            clean_body = clean_html_to_text(html_content or text_content)

            item_text = f"📩 **From:** {sender}\n**Subject:** {subject}\n\n{clean_body}"

            await message.answer(item_text, parse_mode="Markdown")

    @dp.message(F.text.func(lambda t: t and any(w in t.lower() for w in ["удалить", "delete", "🗑"])))
    async def delete_mail(message: Message) -> None:
        user_data = await get_user(message.from_user.id)
        lang = user_data[0] if user_data else "ru"
        
        await clear_user_mailbox(message.from_user.id)
        await message.answer(
            "🗑 Почтовый ящик удален." if lang == "ru" else "🗑 Mailbox deleted.",
            reply_markup=get_main_keyboard(lang)
        )

    app = web.Application()
    setup_webapp_routes(app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', WEBAPP_PORT)
    await site.start()
    logger.info(f"TMA WebApp server started on port {WEBAPP_PORT}")

    async def mail_watcher_worker(bot_instance: Bot) -> None:
        seen_messages: dict[int, set[str]] = {}
        while True:
            try:
                active_users = await get_all_active_users()
                for user_id, _, token in active_users:
                    messages = await get_messages(token)
                    if not messages:
                        continue
                    
                    if user_id not in seen_messages:
                        seen_messages[user_id] = {m.get("id") for m in messages if m.get("id")}
                        continue
                    
                    current_ids = {m.get("id") for m in messages if m.get("id")}
                    new_ids = current_ids - seen_messages[user_id]
                    
                    if new_ids:
                        for msg in messages:
                            msg_id = msg.get("id")
                            if msg_id in new_ids:
                                seen_messages[user_id].add(msg_id)
                                detail = await get_message_detail(token, msg_id) if msg_id else None
                                sender = msg.get("from", {}).get("address", "Unknown")
                                subject = msg.get("subject", "No Subject")
                                html_content = detail.get("html", "") if detail else ""
                                text_content = detail.get("text", "") if detail else msg.get("intro", "")
                                clean_body = clean_html_to_text(html_content or text_content)

                                notification_text = (
                                    f"📬 **New Email Received! / Новое письмо!**\n\n"
                                    f"📩 **From:** {sender}\n"
                                    f"📌 **Subject:** {subject}\n\n"
                                    f"{clean_body}"
                                )
                                try:
                                    await bot_instance.send_message(user_id, notification_text, parse_mode="Markdown")
                                except Exception as e:  # noqa: BLE001
                                    logger.error(f"Failed to send notification to {user_id}: {e}")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Error in mail watcher worker: {e}")
            
            await asyncio.sleep(15)

    asyncio.create_task(mail_watcher_worker(bot))
    logger.info("Starting WastleTempMailBot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
