from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from entities.main.const import WEB_APP_URL

from infra.dbase import db, Database, ConnectionManager

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👇', callback_data='pidor')
        ],
        [
            InlineKeyboardButton(text='Получить прогноз 📊', web_app=WebAppInfo(url=WEB_APP_URL))
        ]
    ]
)

first_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🏆Получить сигнал', callback_data='get_signal')
        ]
    ]
)


async def registr_keyboard():
    async with ConnectionManager(db) as conn:
        url = await conn.fetchval('SELECT referral_url FROM config')
        support_url = await conn.fetchval('SELECT support_url FROM config')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💎 Зарегистрироваться', url=url)
            ],
            [
                InlineKeyboardButton(text='✅ Проверить регистрацию', callback_data=f'check_reg')
            ],
            [
                InlineKeyboardButton(text='🛠 Техподдержка', url=support_url)
            ],

        ]
    )
