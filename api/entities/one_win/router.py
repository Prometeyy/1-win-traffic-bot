from fastapi import APIRouter, Request

from entities.one_win.service import OneWinService

router = APIRouter(
    prefix='/1win'
)


@router.get('/register/{user_id}',)
async def new_one(
        user_id
):
    print(user_id)
    if user_id:
        await OneWinService.add_register(user_id)


@router.get('/deposit/{user_id}',)
async def deposit(
        user_id
):
    print(user_id)
    if user_id:
        await OneWinService.add_deposit(user_id)
