from fastapi import APIRouter

from entities.main.router import router as main_router
from entities.one_win.router import router as one_win_router

router = APIRouter()

router.include_router(main_router)
router.include_router(one_win_router)


