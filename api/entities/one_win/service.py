from infra.dbase import db, ConnectionManager, Database

from datetime import date
from functools import wraps


def check_and_update_date(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with ConnectionManager(self.db) as conn:
            date_old = await conn.fetchval('SELECT today FROM statistic LIMIT 1;')
            date_now = date.today()
            if date_old is not None and date_old < date_now:
                await conn.execute('''
                    UPDATE statistic
                       SET total_deposits   = today_deposits,
                           total_referrals  = today_referrals,
                           today_deposits   = 0,
                           today_referrals  = 0,
                           today            = $1
                ''', date_now)
        return await func(self, *args, **kwargs)

    return wrapper


class OneWinService:

    def __init__(self, db: Database):
        self.db = db

    # @check_and_update_date
    # async def new_one(self):
    #     async with ConnectionManager(self.db) as conn:
    #         await conn.execute('UPDATE statistic SET today_referrals = today_referrals + 1;')
    #
    # @check_and_update_date
    # async def deposit(self, amount: int):
    #     async with ConnectionManager(self.db) as conn:
    #         await conn.execute('UPDATE statistic SET today_deposits = today_deposits + $1;', amount)

    async def add_register(self,
                           user_id):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('INSERT INTO referrals (user_id) VALUES($1) ON CONFLICT DO NOTHING', str(user_id))

    async def add_deposit(self,
                          user_id):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('UPDATE referrals SET deposit = TRUE WHERE user_id = $1', str(user_id))


OneWinService = OneWinService(db)
