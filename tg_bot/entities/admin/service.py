from json import dumps

from infra.dbase import db, Database, ConnectionManager


class AdminService:

    def __init__(self,
                 db: Database):
        self.db = db

    async def update_lucky_get_signals(self,
                                       file_text: str):
        file_text = file_text.replace(',', '.').splitlines()
        numbers = []
        for i in range(len(file_text)):
            try:
                numbers.append(
                    float(file_text[i])
                )

            except ValueError:
                return f'Ошибка в {i + 1} строчке файла'
        numbers = dumps(numbers)
        async with ConnectionManager(self.db) as conn:
            await conn.execute('UPDATE lucky_jet_signals SET signals = $1 WHERE TRUE', numbers)
        return True

    async def get_statistic(self):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchrow('SELECT * FROM statistic WHERE TRUE;')

    async def update_referral_url(self,
                                  url: str):
        async with ConnectionManager(self.db) as conn:
            return await conn.execute('UPDATE config SET referral_url = $1 WHERE TRUE;', url)

    async def update_support_url(self,
                                 url: str):
        async with ConnectionManager(self.db) as conn:
            return await conn.execute('UPDATE config SET support_url = $1 WHERE TRUE;', url)

    async def get_referral(self):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchval('SELECT referral_url FROM config')

    # ================ #
    async def check_question_available(self,
                                       question: str,
                                       question_type: str):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetchval('SELECT EXISTS (SELECT 1 FROM faq WHERE question = $1 AND type = $2);', question,
                                       question_type)

    async def add_question(self,
                           question: str,
                           question_type: str,
                           answer: str,
                           question_lang: str
                           ):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('INSERT INTO faq (question, type, answer, lang) VALUES ($1,$2,$3,$4)', question,
                               question_type,
                               answer, question_lang)

    async def del_question(self,
                           question_id
                           ):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('DELETE FROM faq WHERE id = $1', question_id)

    async def get_faq(self,
                      faq_types: str,
                      faq_lang: str):
        async with ConnectionManager(self.db) as conn:
            result = await conn.fetch('SELECT * FROM faq WHERE type = $1 AND lang = $2;', faq_types, faq_lang)
            faqs = []
            for faq in result:
                faqs.append({
                    'id': faq['id'],
                    'question': faq['question'],
                    'answer': faq['answer']
                })

            return faqs

    async def get_admin_list(self):
        async with ConnectionManager(self.db) as conn:
            return await conn.fetch('SELECT tg_id FROM admins')

    async def del_admin(self,
                        tg_id: int):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('DELETE FROM admins WHERE tg_id = $1', tg_id)

    async def add_admin(self,
                        tg_id: int):
        async with ConnectionManager(self.db) as conn:
            await conn.execute('INSERT INTO admins (tg_id) VALUES($1) ON CONFLICT DO NOTHING;', tg_id)


AdminService = AdminService(db)
