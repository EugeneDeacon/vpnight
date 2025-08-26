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
