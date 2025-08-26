from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, Message
from src.services.users import UserService
from src.keyboards.lk import lk_keyboard
from src.constants import ASSETS_DIR, Texts

router = Router()

@router.callback_query(F.data == "personal_account")
async def on_personal_account(query: CallbackQuery, bot: Bot):
    photo_path = ASSETS_DIR / "1.webp"

    async with UserService() as service:
        db_user = await service.get_by_id(query.from_user.id)

    if not db_user:
        raise ValueError("Пользователь не найден")

    text = Texts.LK.format(
        user_id=db_user.id,
        username=db_user.username or "Не указан",
        balance=db_user.balance
    )

    if query.message is not None and isinstance(query.message, Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=FSInputFile(photo_path),
        caption=text,
        parse_mode="Markdown",
        reply_markup=lk_keyboard
    )

    await query.answer()
