from aiogram import Bot, Dispatcher, Router

from asyncio import run

from const import BOT_API_TOKEN

from router import router

from infra.dbase import db, Database


def build_bot(
        router: Router,
        BOT_API_TOKEN: str
):
    bot = Bot(BOT_API_TOKEN)

    dp = Dispatcher()
    dp.include_router(router)
    return dp, bot


async def on_startup():
    # Запуск доп сервисов - бд, редис и тд
    await db.init_pool()


async def run_bot(
        dp, bot
):
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(
        run_bot(
            *build_bot(router, BOT_API_TOKEN)
        )
    )
