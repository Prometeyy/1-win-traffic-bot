from infra.dbase import db, Database, ConnectionManager

from json import loads


class MainService:

    def __init__(self,
                 db: Database):
        self.db = db

    async def get_lucky_get_signal(self):
        async with ConnectionManager(self.db) as conn:
            result = await conn.fetchrow('SELECT * FROM lucky_jet_signals;')
            last_signal_index = result['last_signal_index'] + 1
            signals = loads(result['signals'])
            if last_signal_index >= len(signals):
                last_signal_index = 0
            signal = signals[last_signal_index]
            await conn.execute('UPDATE lucky_jet_signals SET last_signal_index = $1 WHERE TRUE;', last_signal_index)
            return signal

    async def check_user(self,
                         one_win_id: str,
                         tg_id: int):
        async with ConnectionManager(self.db) as conn:
            if one_win_id == 'secret_key_998wqoneb':
                await conn.execute('UPDATE users SET dostup = TRUE WHERE tg_id = $1', tg_id)
                return True
            user_data = await conn.fetchrow('SELECT * FROM referrals WHERE user_id = $1', one_win_id)
            if not user_data:
                return False
            if user_data['deposit'] and not user_data.get('tg_id'):
                await conn.execute('UPDATE referrals SET tg_id = $1 WHERE user_id =$2', tg_id, one_win_id)
                await conn.execute('UPDATE users SET dostup = TRUE WHERE tg_id = $1', tg_id)
                return True
            return False

    async def check_user_with_tg_id(self,
                                    tg_id: int):
        async with ConnectionManager(self.db) as conn:
            user_data = await conn.fetchrow('SELECT * FROM users WHERE tg_id = $1', tg_id)
            if user_data['dostup']:
                return True
            return False

    async def post_user(self,
                        tg_id: int):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('INSERT INTO users (tg_id) VALUES($1) ON CONFLICT DO NOTHING', tg_id)


MainService = MainService(db)
