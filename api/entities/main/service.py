from random import shuffle, choice

from json import loads

from entities.main.dto import Faq, FaqTypes, FaqLang

from infra.dbase import db, ConnectionManager, Database


class MainService:

    def __init__(self,
                 db: Database):
        self.db = db

    async def get_support(self):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchval('SELECT support_url FROM config')

    async def get_referral(self):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchval('SELECT referral_url FROM config')

    async def get_faq(self,
                      faq_types: FaqTypes,
                      faq_lang: FaqLang):
        async with ConnectionManager(self.db) as conn:
            result = await conn.fetch('SELECT * FROM faq WHERE type = $1 AND lang = $2;', faq_types.value,
                                      faq_lang.value)
            faqs = []
            for faq in result:
                faqs.append(
                    Faq(
                        question=faq['question'],
                        answer=faq['answer']
                    ).dict()
                )
            return faqs

    async def get_lucky_get_signal(self):
        async with ConnectionManager(self.db) as conn:
            result = await conn.fetchrow('SELECT * FROM lucky_jet_signals;')
            result = loads(result['signals'])
            return choice(result)

    @staticmethod
    def get_mines_signal(mines: int):
        values = [True] * mines + [False] * (25 - mines)
        shuffle(values)
        return [values[i:i + 5] for i in range(0, 25, 5)]


MainService = MainService(db)
