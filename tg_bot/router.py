from aiogram import Router

from entities.main.router import router as main_router
from entities.admin.router import router as admin_router

router = Router()

router.include_router(admin_router)
#
router.include_router(main_router)
