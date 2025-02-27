from aiogram.types import Message
from aiogram.filters import BaseFilter

from infra.dbase import db, Database, ConnectionManager


class IsAdmin(BaseFilter):
    db: Database = db

    async def __call__(self, message: Message):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchval('SELECT EXISTS (SELECT 1 FROM admins WHERE tg_id = $1);', message.from_user.id)
