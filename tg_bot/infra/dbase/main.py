from asyncpg import create_pool, Connection, Pool

from pathlib import Path

from infra.dbase.const import DSN


class Database:
    def __init__(self, dsn: str, max_size: int = 10):
        self.dsn = dsn
        self.max_size = max_size
        self.pool = None

    def build_sql_init_file(self,
                            base_path='entities',
                            main_path='infra/dbase/init.sql'):
        base_path = Path(base_path)
        sql_files = [f for f in base_path.rglob('*.sql')]

        tables_sql_file = Path(main_path)
        with tables_sql_file.open('w', encoding='utf-8') as file:
            for sql_file in sql_files:
                with sql_file.open('r', encoding='utf-8') as infile:
                    file.write(f'{"-" * 8} {sql_file.name.rstrip(".sql").upper()} {"-" * 8} \n')
                    file.write(infile.read())
                    file.write('\n\n')

    async def init_tables(self,
                          main_path='infra/dbase/init.sql'
                          ):
        with open(main_path, 'r') as file:
            sql = file.read()
        async with self.pool.acquire() as connection:
            await connection.execute(sql)

    async def init_pool(self):
        self.pool = await create_pool(dsn=self.dsn, max_size=self.max_size)

    async def close_pool(self):
        if self.pool:
            await self.pool.close()


class ConnectionManager:
    def __init__(self, db: Database):
        self.db = db

    async def __aenter__(self):
        self.connection: Connection = await self.db.pool.acquire()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.pool.release(self.connection)


class TransactionManager:
    def __init__(self, connection):
        self.connection: Connection = connection

    async def __aenter__(self):
        self.transaction = self.connection.transaction()
        await self.transaction.start()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.transaction.rollback()
        else:
            await self.transaction.commit()


db = Database(DSN)
