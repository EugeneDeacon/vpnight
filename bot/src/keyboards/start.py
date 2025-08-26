from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # 1-я строка
        [InlineKeyboardButton(text="🛡 Мой VPN", callback_data="my_vpn")],

        # 2-я строка
        [InlineKeyboardButton(text="👤 Личный кабинет", callback_data="personal_account")],

        # 3-я строка (ссылки)
        [
            InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/support_channel"),
            InlineKeyboardButton(text="📢 Канал", url="https://t.me/news_channel")
        ],

        # 4-я строка
        [InlineKeyboardButton(text="❓ FAQ", callback_data="faq")]
    ]
)
