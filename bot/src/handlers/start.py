from aiogram import Router, types, F, Bot
from aiogram.types import FSInputFile
from aiogram.filters import Command, CommandObject

from src.services.notification import NotificationService
from src.services.users import UserService
from src.constants import ASSETS_DIR, Texts
from src.keyboards.start import start_keyboard


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject, notifications: NotificationService):
    """
    Отрабатывает при старте бота, регистрирует пользователя, отправляет приветственное сообщение
    """

    photo_path = ASSETS_DIR / "1.png"
    payload: str | None = command.args

    user: types.User | None = message.from_user
    if user is None or user.is_bot:
        return


    if command.args:
        payload = command.args

    user_info = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
    }

    if payload:
        try:
            async with UserService() as service:
                referrer = await service.get_by_id(int(payload))
            user_info["referrer_id"] = int(payload)

            if referrer:
                await notifications.send_message(chat_id=referrer.id, text=Texts.NEW_REFERRER)
        except ValueError as e:
            await message.answer_photo(
                photo=FSInputFile(photo_path),
                caption=Texts.ERROR,
            )
            return

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


@router.callback_query(F.data == "main_menu")
async def on_main_menu(query: types.CallbackQuery, bot: Bot):
    """Отправляет главное меню при переходе с других страниц"""

    photo_path = ASSETS_DIR / "1.png"

    if query.message is not None and isinstance(query.message, types.Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=FSInputFile(photo_path),
        caption=Texts.WELCOME,
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )

    await query.answer()
