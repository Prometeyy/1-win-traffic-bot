from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from entities.main.const import WEB_APP_URL

# admin_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='🗂Статистика📊', callback_data='statistic')
#         ],
#         [
#             InlineKeyboardButton(text='📎Изменить реф. ссылку', callback_data='update_referral_url')
#         ],
#         [
#             InlineKeyboardButton(text='Изменить ссылку на саппорта🔗', callback_data='update_partner_url')
#         ],
#         [
#             InlineKeyboardButton(text='📣Обновить сигналы LuckyJet', callback_data='update_lucky_get_signals')
#         ],
#         [
#             InlineKeyboardButton(text='Добавить вопрос в faq❓', callback_data='update_faq')
#         ],
#         [
#             InlineKeyboardButton(text='✅Добавить админа', callback_data='add_admin'),
#             InlineKeyboardButton(text='Удалить админа❌', callback_data='del_admin')
#         ],
#         [
#             InlineKeyboardButton(text='📜Список админов', callback_data='admin_list'),
#         ],
#
#     ]
# )
#
# admin_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Статистика', callback_data='statistic')
#         ],
#         [
#             InlineKeyboardButton(text='Изменить реф. ссылку', callback_data='update_referral_url')
#         ],
#         [
#             InlineKeyboardButton(text='Изменить ссылку на саппорта', callback_data='update_partner_url')
#         ],
#         [
#             InlineKeyboardButton(text='Обновить сигналы LuckyJet', callback_data='update_lucky_get_signals')
#         ],
#         [
#             InlineKeyboardButton(text='Добавить вопрос в faq', callback_data='update_faq')
#         ],
#         [
#             InlineKeyboardButton(text='Добавить админа', callback_data='add_admin'),
#             InlineKeyboardButton(text='Удалить админа', callback_data='del_admin')
#         ],
#         [
#             InlineKeyboardButton(text='Список админов', callback_data='admin_list'),
#         ],
#
#     ]
# )

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text='🗂Статистика📊', callback_data='statistic')
        # ],
        [
            InlineKeyboardButton(text='📎Изменить реф. ссылку', callback_data='update_referral_url')
        ],
        [
            InlineKeyboardButton(text='🔗Изменить ссылку на саппорта', callback_data='update_support_url')
        ],
        [
            InlineKeyboardButton(text='📣Обновить сигналы LuckyJet', callback_data='update_lucky_get_signals')
        ],
        [
            InlineKeyboardButton(text='❓Добавить вопрос в faq', callback_data='update_faq')
        ],
        [
            InlineKeyboardButton(text='🔪Удалить вопрос faq', callback_data='delete_faq')
        ],
        [
            InlineKeyboardButton(text='📜Список админов', callback_data='admin_list'),
        ],

    ]
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить ❌', callback_data='cancel')
        ],
    ]
)

back_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Админ панель📭', callback_data='admin_back')
        ]
    ]
)

add_faq_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Для главной страницы', callback_data='add_faq_question_main')
        ],
        [
            InlineKeyboardButton(text='Для страницы с играми', callback_data='add_faq_question_game')
        ]
    ]
)

select_faq_lang_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский', callback_data='select_faq_lang:ru'),
            InlineKeyboardButton(text='Английский', callback_data='select_faq_lang:en')
        ],
        [
            InlineKeyboardButton(text='Хинди', callback_data='select_faq_lang:hi'),
            InlineKeyboardButton(text='Узбекский', callback_data='select_faq_lang:uz')
        ]
    ]
)


def delete_faq_lang_kb(question_type):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Русский', callback_data=f'del_faq_lang:ru:{question_type}'),
                InlineKeyboardButton(text='Английский', callback_data=f'del_faq_lang:en:{question_type}')
            ],
            [
                InlineKeyboardButton(text='Хинди', callback_data=f'del_faq_lang:hi:{question_type}'),
                InlineKeyboardButton(text='Узбекский', callback_data=f'del_faq_lang:uz:{question_type}')
            ]
        ]
    )


def faq_show(
        faq_id,
        faq_type,
        i,
        last_i,
        faq_lang
):

    inline_keyboard = [
        [
            InlineKeyboardButton(text='Удалить ❌', callback_data=f'kill_faq:{faq_id}'),
        ]
    ]
    if last_i == 0:
        ...
    elif i == last_i:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='⬅️', callback_data=f'kill_faq_next:{i - 1}:{faq_lang}:{faq_type}'),
            ],
        )
    elif i == 0:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='➡️', callback_data=f'kill_faq_next:{i + 1}:{faq_lang}:{faq_type}'),
            ],
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='⬅️', callback_data=f'kill_faq_next:{i - 1}:{faq_lang}:{faq_type}'),
                InlineKeyboardButton(text='➡️', callback_data=f'kill_faq_next:{i + 1}:{faq_lang}:{faq_type}'),
            ],
        )

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


del_faq_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Для главной страницы', callback_data='del_faq_question_main')
        ],
        [
            InlineKeyboardButton(text='Для страницы с играми', callback_data='del_faq_question_game')
        ]
    ]
)


def admin_list_kb(admins):
    inline_keyboard = []
    for admin in admins:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=f'{admin["tg_id"]}', callback_data='pidor'),
                InlineKeyboardButton(text=f'Удалить ❌', callback_data=f'del_admin:{admin["tg_id"]}'),
            ]
        )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=f'Добавить админа✅', callback_data='add_admin'),
        ]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
