from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import load_settings


cfg = load_settings()

full_price = cfg.price_1 * 3


discount_percent = round((full_price - cfg.price_3) / full_price * 100, 2)

def get_my_vpn_keyboard(vpn_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # 1-я строка
            [InlineKeyboardButton(text="🔐 Настроить VPN", url=vpn_url)],

            # 2-я строка
            [InlineKeyboardButton(text="💳 Продлить", callback_data="extend")],

            # 3-я строка
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
        ]
    )


vpn_extend_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # 1-я строка
        [InlineKeyboardButton(text=f"1 месяц - {cfg.price_1}р", callback_data="extend_1")],

        # 2-я строка
        [InlineKeyboardButton(text=f"3 месяца - {cfg.price_3}р (-{discount_percent}%)", callback_data="extend_3")],

        # 3-я строка
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="my_vpn")]
    ]
)
