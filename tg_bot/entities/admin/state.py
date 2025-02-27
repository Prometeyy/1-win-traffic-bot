from aiogram.filters.state import State, StatesGroup


class LuckyJetSignal(StatesGroup):
    txt_file = State()


class UpdateReferralUrl(StatesGroup):
    url = State()


class UpdateSupportUrl(StatesGroup):
    url = State()


class SelectFaqQuestion(StatesGroup):
    language = State()
    # ru, en, uz, hi


class AddFaqQuestion(StatesGroup):
    question = State()


class AddFaqAnswer(StatesGroup):
    answer = State()


class DelFaqQuestion(StatesGroup):
    question = State()


class AddAdmin(StatesGroup):
    admin_id = State()
