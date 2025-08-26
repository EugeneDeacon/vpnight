from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.filters import Command

from src.services.users import UserService
from src.constants import ASSETS_DIR, Texts
from src.keyboards.start import start_keyboard


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    photo_path = ASSETS_DIR / "main.png"

    user: types.User | None = message.from_user
    if user is None or user.is_bot:
        return

    user_info = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
    }

    async with UserService() as service:
        db_user = await service.register(user_info)

    if not db_user:
        return

    await message.answer_photo(
        photo=FSInputFile(photo_path),
        caption=Texts.WELCOME,
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )
