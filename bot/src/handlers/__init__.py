from aiogram import Dispatcher

from .start import router as start_router
from .lk import router as lk_router
from .vpn import router as vpn_router


def register_handlers(dp: Dispatcher):
    """ Подключает все роутеры. """
    dp.include_router(start_router)
    dp.include_router(lk_router)
    dp.include_router(vpn_router)
