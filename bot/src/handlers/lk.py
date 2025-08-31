from decimal import Decimal
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, Message
from src.services.gotify import GotifyService
from config import load_settings
from src.services.users import UserService
from src.keyboards.lk import lk_keyboard, success_top_up_keyboard, lk_ref_keyboard, lk_top_up_keyboard
from src.constants import ASSETS_DIR, Texts
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

class TopUpStates(StatesGroup):
    waiting_for_amount = State()

@router.callback_query(F.data == "personal_account")
async def on_personal_account(query: CallbackQuery, bot: Bot):
    photo_path = ASSETS_DIR / "2.png"

    async with UserService() as service:
        db_user = await service.get_by_id(query.from_user.id)

    if not db_user:
        raise ValueError("Пользователь не найден")

    text = Texts.LK.format(
        user_id=db_user.id,
        username=db_user.username or "Не указан",
        balance=float(db_user.balance) or 0.0
    )

    if query.message is not None and isinstance(query.message, Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=FSInputFile(photo_path),
        caption=text,
        parse_mode="HTML",
        reply_markup=lk_keyboard
    )

    await query.answer()


@router.callback_query(F.data == "ref_program")
async def on_ref_program(query: CallbackQuery, bot: Bot):
    photo_path = ASSETS_DIR / "6.png"

    async with UserService() as service:
        db_user = await service.get_by_id(query.from_user.id)

    if not db_user:
        raise ValueError("Пользователь не найден")

    cfg = load_settings()

    text = Texts.REF.format(
        bot_url=cfg.bot_url,
        user_id=db_user.id,
        users_count=len(db_user.referrals)

    )

    if query.message is not None and isinstance(query.message, Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=FSInputFile(photo_path),
        caption=text,
        parse_mode="HTML",
        reply_markup=lk_ref_keyboard
    )

    await query.answer()



@router.callback_query(F.data == "top_up")
async def on_top_up(query: CallbackQuery, bot: Bot):
    photo_path = ASSETS_DIR / "1.webp"

    if query.message is not None and isinstance(query.message, Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=FSInputFile(photo_path),
        caption=Texts.TOP_UP,
        parse_mode="HTML",
        reply_markup=lk_top_up_keyboard
    )

    await query.answer()


@router.callback_query(F.data == "top_up_sbp")
async def top_up_sbp(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите сумму для пополнения:")
    await state.set_state(TopUpStates.waiting_for_amount)
    await query.answer()


@router.message(TopUpStates.waiting_for_amount)
async def process_top_up_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное число.")
        return

    async with UserService() as service:
        db_user = await service.get_by_id(message.from_user.id)

        await service.update_user(id=db_user.id, fields={"balance": Decimal(db_user.balance) + Decimal(amount)})
    if db_user is None:
        await message.answer("❌ Пользователь не найден.")
        return

    await message.answer(f"Вы пополнили {amount:.2f} RUB через СБП ✅", reply_markup=success_top_up_keyboard)

    async with GotifyService() as service:
        user_identifier = db_user.username if db_user.username is not None else db_user.id
        await service.send_message(message=f"Пользователь {user_identifier} пополнил баланс на {amount:.2f} RUB", title="Пополнение баланса", priority=5)

    await state.clear()
