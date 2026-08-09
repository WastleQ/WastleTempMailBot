from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from config import WEBAPP_URL
from locales import get_text


def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    rows = [
        [
            KeyboardButton(text=get_text(lang, "btn_create")),
            KeyboardButton(text=get_text(lang, "btn_check")),
        ]
    ]
    if WEBAPP_URL and WEBAPP_URL.startswith("https://"):
        rows.append([
            KeyboardButton(text=get_text(lang, "btn_webapp"), web_app=WebAppInfo(url=WEBAPP_URL))
        ])
    rows.append([
        KeyboardButton(text=get_text(lang, "btn_status")),
        KeyboardButton(text=get_text(lang, "btn_delete")),
        KeyboardButton(text=get_text(lang, "btn_lang")),
    ])
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
    )

def get_lang_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )
