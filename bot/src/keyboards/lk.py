from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


lk_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # 1-я строка
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="top_up")],

        # 2-я строка
        [InlineKeyboardButton(text="👥 Реферальная программа", callback_data="ref_program")],

        # 3-я строка
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ]
)

lk_ref_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="⬅️ Назад", callback_data="personal_account")]
    ]
)

lk_top_up_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="СБП", callback_data="top_up_sbp")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="personal_account")]
    ]
)


success_top_up_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # 1-я строка
        [InlineKeyboardButton(text="🛡 Мой VPN", callback_data="my_vpn")],

        # 2-я строка
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ]
)
