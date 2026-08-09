
TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "welcome": (
            "🔐 **WastleTempMailBot** — Анонимная временная почта для любых сервисов.\n\n"
            "• Почта создается на 15 минут.\n"
            "• Получение писем в реальном времени.\n"
            "• Полная конфиденциальность в экосистеме Wastle.\n\n"
            "Выберите действие ниже:"
        ),
        "choose_lang": "🌐 Выберите язык / Choose your language:",
        "lang_set": "✅ Язык успешно изменен на русский.",
        "btn_create": "✉️ Создать почту",
        "btn_check": "🔄 Проверить входящие",
        "btn_delete": "🗑 Удалить почту",
        "btn_lang": "🌐 Сменить язык",
        "btn_webapp": "🌐 Открыть WebApp",
        "btn_status": "📊 Статус почты",
        "no_mail": "❌ У вас нет активного почтового ящика. Нажмите «Создать почту».",
        "status_active": "📮 **Ваш текущий почтовый ящик:**\n`{email}`\n\nИспользуйте меню ниже для проверки писем или управления:",
        "status_none": "❌ У вас нет активного почтового ящика. Нажмите «Создать почту».",
        "mail_created": (
            "✅ **Ваш временный ящик создан:**\n\n"
            "`{email}`\n\n"
            "⏳ Срок действия: 15 минут.\n"
            "Нажмите «Проверить входящие», когда ждете письмо."
        ),
        "inbox_empty": "📭 Входящих писем пока нет.",
        "inbox_header": "📬 **Входящие письма ({count}):**\n\n",
        "code_found": "🔑 **Найденный код подтверждения:** `{code}`\n",
        "btn_verify_link": "🔗 Подтвердить почту",
        "message_item": "📩 **От:** {sender}\n**Тема:** {subject}\n\n{body}\n\n",
    },
    "en": {
        "welcome": (
            "🔐 **WastleTempMailBot** — Anonymous temporary email for any service.\n\n"
            "• Mailbox lasts for 15 minutes.\n"
            "• Real-time message reception.\n"
            "• Full confidentiality in the Wastle ecosystem.\n\n"
            "Choose an action below:"
        ),
        "choose_lang": "🌐 Choose your language / Выберите язык:",
        "lang_set": "✅ Language successfully changed to English.",
        "btn_create": "✉️ Create Mail",
        "btn_check": "🔄 Check Inbox",
        "btn_delete": "🗑 Delete Mail",
        "btn_lang": "🌐 Change Language",
        "btn_webapp": "🌐 Open WebApp",
        "btn_status": "📊 Mail Status",
        "no_mail": "❌ You don't have an active mailbox. Click «Create Mail».",
        "status_active": "📮 **Your active mailbox:**\n`{email}`\n\nUse the menu below to check inbox or manage:",
        "status_none": "❌ You don't have an active mailbox. Click «Create Mail».",
        "mail_created": (
            "✅ **Your temporary mailbox is ready:**\n\n"
            "`{email}`\n\n"
            "⏳ Lifespan: 15 minutes.\n"
            "Click «Check Inbox» when waiting for a message."
        ),
        "inbox_empty": "📭 Inbox is empty.",
        "inbox_header": "📬 **Inbox ({count}):**\n\n",
        "code_found": "🔑 **Found verification code:** `{code}`\n",
        "btn_verify_link": "🔗 Verify Email",
        "message_item": "📩 **From:** {sender}\n**Subject:** {subject}\n\n{body}\n\n",
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    lang_dict = TEXTS.get(lang, TEXTS["ru"])
    text = lang_dict.get(key, TEXTS["ru"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
