from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from entities.main.service import MainService
from entities.main.keyboard import *

from aiogram.filters.state import State, StatesGroup


class CheckReg(StatesGroup):
    check = State()


router = Router()


@router.message(StateFilter(default_state), CommandStart)
async def start(message: Message):
    await MainService.post_user(message.from_user.id)
    await message.answer(
        text=f"""👋 Приветствую тебя <b><i>{"@" + message.from_user.username if message.from_user.username else message.from_user.first_name}</i></b>

❓Для чего нужен наш бот?
• С его помощью ты сможешь получить сигналы полученные алгоритмом разработанным нашей командой на такие игры как: LuckyJet, 1WinMines, Mines 🔥

❓Как получить сигнал?
•  Заходи в бот по кнопке с низу, выбирай свою любимую игру и зарабатывай вместе с нами! 💸""",
        reply_markup=first_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'get_signal')
async def get_signal(callback: CallbackQuery):
    if await MainService.check_user_with_tg_id(callback.from_user.id):
        await callback.message.edit_text(text="""💸 Теперь ты можешь пользоваться современным инструментом для заработка на 1win!

💎 Быстрее заходи в софт и получай первый профит вместе с нами!""",
                                         reply_markup=start_keyboard)
    else:
        await callback.message.edit_text(
            text="""❌ Ой-ой... похоже ты еще не зарегистрировался на сайте...

💸 Чтобы получить доступ к софту, зарегистрируйся по промокоду <b><i>MONEYCURRENCY</i></b> и сделай свой первый депозит!""",
            reply_markup=await registr_keyboard(),
            parse_mode='HTML'
        )


@router.callback_query(F.data == 'check_reg')
async def check_reg(callback: CallbackQuery,
                    state: FSMContext):
    await state.set_state(CheckReg.check)
    await callback.message.edit_text('📣 Чтобы проверить выполнение условий, пришлите свой 1win id')


@router.message(CheckReg.check)
async def check_reg_finally(message: Message, state: FSMContext):
    one_win_id = message.text
    if await MainService.check_user(one_win_id, message.from_user.id):
        await state.clear()
        await message.answer(text="""💸 Теперь ты можешь пользоваться современным инструментом для заработка на 1win!

💎 Быстрее заходи в софт и получай первый профит вместе с нами!""",
                             reply_markup=start_keyboard)
    else:
        await message.answer(
            text="""⚙️ Ой-ой мы не нашли такой 1win id в нашей базе... 
            
❌Похоже ты еще не зарегистрировался на сайте или не сделал свой депозит

💎Попробуй еще раз или подожди еще немного, пока наша система найдет тебя!""",
            reply_markup=await registr_keyboard()
        )


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Отменено')
