from datetime import datetime, timezone
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from aiogram import Bot, Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from marzban.models import UserResponse

from src.services.notification import NotificationService
from src.services.gotify import GotifyService
from config import load_settings
from src.services.users import UserService
from src.services.marzban import MarzbanService
from src.keyboards.vpn import get_my_vpn_keyboard, vpn_extend_keyboard
from src.constants import ASSETS_DIR, Texts


class ExtendStates(StatesGroup):
    waiting_for_period = State()

router = Router()

@router.callback_query(F.data == "my_vpn")
async def on_my_vpn(query: types.CallbackQuery, bot: Bot):
    """Выдает информацию о VPN пользователе"""


    photo_path = ASSETS_DIR / "3.png"

    async with MarzbanService() as service:
        # Получение информации о пользователе
        marzban_user: UserResponse | None = await service.get_user(query.from_user.id)

    # Проверка на наличие пользователя и его данных
    if marzban_user is None or marzban_user.expire is None or marzban_user.subscription_url is None:
        raise ValueError("User not found")

    # Форматирование даты окончания подписки
    expire_dt = datetime.fromtimestamp(marzban_user.expire, tz=timezone.utc)
    expire_str = expire_dt.strftime("%d-%m-%Y")

    status_text = "Активирован" if marzban_user.status == "active" else "Неактивен"

    # Формирование текста сообщения
    text = Texts.MY_VPN.format(
        status=status_text,
        end_date=expire_str
    )

    if query.message is not None and isinstance(query.message, types.Message):
        await query.message.delete()

    await bot.send_photo(
        chat_id=query.from_user.id,
        photo=types.FSInputFile(photo_path),
        caption=text,
        parse_mode="HTML",
        reply_markup=get_my_vpn_keyboard(marzban_user.subscription_url)
    )

    await query.answer()


@router.callback_query(F.data == "extend")
async def extend(query: types.InputMediaUnion, state: FSMContext):
    await state.clear()

    if query.message is not None and isinstance(query.message, types.Message):
        await query.message.delete()

    await query.message.answer(
        "Выберите период пополнения:",
        reply_markup=vpn_extend_keyboard
    )
    await state.set_state(ExtendStates.waiting_for_period)
    await query.answer()



@router.callback_query(F.data.startswith("extend_"))
async def handle_extend_period(query: types.CallbackQuery, state: FSMContext, notifications: NotificationService):

    cfg = load_settings()

    prices = {
        1: cfg.price_1,
        3: cfg.price_3,
    }

    period = query.data.split("_")[1]
    months_to_add = int(period)

    async with UserService() as service:
        # Получение пользователя из базы данных по ID
        db_user = await service.get_by_id(query.from_user.id)

    if not db_user:
        await state.clear()
        raise ValueError("Пользователь не найден")

    price = prices.get(months_to_add)
    if price is None:
        await state.clear()
        await query.message.answer("Неверный период")
        return

    if db_user.balance < price:
        await state.clear()
        await query.message.answer("Недостаточно средств")
        return


    async with MarzbanService() as service:
        # Получение информации о пользователе
        marzban_user: UserResponse | None = await service.get_user(query.from_user.id)

    # Проверка на наличие пользователя и его данных
    if marzban_user is None or marzban_user.expire is None or marzban_user.subscription_url is None:
        raise ValueError("User not found")
        return


    # Из timestamp в datetime
    expire_dt = datetime.fromtimestamp(marzban_user.expire, tz=timezone.utc)

    # Прибавляем месяцы
    new_expire_dt = expire_dt + relativedelta(months=months_to_add)

    # Обратно в timestamp
    new_expire_ts = int(new_expire_dt.timestamp())

    async with UserService() as service:
        updated_user = await service.update_user(id=db_user.id, fields={"balance": Decimal(db_user.balance) - Decimal(price)})

    if updated_user is None:
        await query.message.answer("Ошибка обновления баланса")
        return

    async with MarzbanService() as service:
        updated_sub = await service.update_expire(db_user.id, new_expire_ts)

    if updated_sub is None:
        await query.message.answer("Ошибка обновления подписки")
        return

    await query.message.answer(f"Вы продлили на {period} месяцев")

    async with GotifyService() as service:
        user_identifier = updated_user.username if updated_user.username is not None else updated_user.id
        await service.send_message(message=f"Пользователь {user_identifier} продлил подписку на {period} месяцев", title="Продление подписки", priority=5)

    if updated_user.referrer_id is None:
        return

    async with UserService() as service:
        referrer = await service.get_by_id(id=updated_user.referrer_id)

    if referrer is None:
        return

    async with MarzbanService() as service:
        referrer_sub: UserResponse | None = await service.get_user(referrer.id)

    if referrer_sub is None or referrer_sub.expire is None:
        return

    # Из timestamp в datetime
    ref_expire_dt = datetime.fromtimestamp(referrer_sub.expire, tz=timezone.utc)

    # Прибавляем месяцы
    ref_new_expire_dt = ref_expire_dt + relativedelta(days=round(30 * 0.15 * months_to_add))

    # Обратно в timestamp
    ref_new_expire_ts = int(ref_new_expire_dt.timestamp())

    async with MarzbanService() as service:
        updated_ref_sub = await service.update_expire(referrer.id, ref_new_expire_ts)

    if updated_ref_sub is None:
        return

    text = Texts.EXTEND_REF.format(
        days=round(30 * 0.15 * months_to_add),
    )

    await notifications.send_message(chat_id=referrer.id, text=text)


    await state.clear()
