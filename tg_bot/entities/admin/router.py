from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from entities.admin.filter import IsAdmin
from entities.admin.keyboard import *
from entities.admin.state import LuckyJetSignal, UpdateReferralUrl, UpdateSupportUrl, AddFaqQuestion, AddFaqAnswer, \
    DelFaqQuestion, AddAdmin, SelectFaqQuestion
from entities.admin.service import AdminService

router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == 'admin_back')
async def admin(callback: CallbackQuery):
    await callback.message.edit_text(
        text='🛠 Добро пожаловать в админ панель 🛠 ',
        reply_markup=admin_kb
    )


@router.message(Command('admin'))
async def admin(message: Message):
    await message.answer(
        text='🛠 Добро пожаловать в админ панель 🛠 ',
        reply_markup=admin_kb
    )


# ================ #
@router.callback_query(F.data == 'update_lucky_get_signals')
async def update_lucky_get_signals(callback: CallbackQuery,
                                   state: FSMContext):
    await state.set_state(LuckyJetSignal.txt_file)
    await callback.message.edit_text(
        text='• Пришлите файл .txt с сигналами на LuckyJet.\n'
             'Пример входного файла:\n<blockquote>'
             '4.57\n'
             '1.12\n'
             '2.56\n'
             '12.45\n'
             '...\n</blockquote>'
             '• Каждый коэфицент с новой строчки, если хотите написать целое число ставьте точку между знаками.',
        reply_markup=cancel_kb,
        parse_mode='HTML'
    )


@router.message(LuckyJetSignal.txt_file)
async def confirm_update_lucky_get_signals(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    if message.document:
        document = message.document
        if document.mime_type == 'text/plain':
            file = await bot.get_file(document.file_id)
            downloaded_file = await bot.download_file(file.file_path)
            downloaded_file.seek(0)
            file_text = downloaded_file.read().decode('utf-8', errors='replace')

            res = await AdminService.update_lucky_get_signals(file_text)
            if isinstance(res, bool):
                await state.clear()
                await message.answer('Коэфиценты обновлены!', reply_markup=back_admin_kb)
            else:
                await message.answer('Файл содержит неверный формат!\n'
                                     f'{res}\n'
                                     f'Попробуйте снова', reply_markup=cancel_kb)
        else:
            await message.answer('Вы отправили боту файл другого формата, отправьте .txt и попробуйте снова',
                                 reply_markup=cancel_kb)
    else:
        await message.answer('В сообщение не нашли .txt файл,попробуйте снова', reply_markup=cancel_kb)


# ================ #
@router.callback_query(F.data == 'statistic')
async def statistic(callback: CallbackQuery):
    statistic_info = await AdminService.get_statistic()
    await callback.message.edit_text(
        text=f'Статистика на {statistic_info["today"]}\n'
             f'\n'
             f'<b>Заработок:</b>\n'
             f'\t\t• все время: <i>{statistic_info["total_deposits"]}</i>\n'
             f'\t\t• сегодня: <i>{statistic_info["today_deposits"]}</i>\n'
             f'\n'
             f'<b>Регистраций:</b>\n'
             f'\t\t• все время: <i>{statistic_info["total_referrals"]}</i>\n'
             f'\t\t• сегодня: <i>{statistic_info["today_referrals"]}</i>\n',
        parse_mode='HTML',
        reply_markup=back_admin_kb
    )


# ================ #
@router.callback_query(F.data == 'update_referral_url')
async def update_referral_url(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateReferralUrl.url)
    await callback.message.edit_text(
        'Пришлите новую реф ссылку на партнерку 1win',
        reply_markup=cancel_kb
    )


@router.message(UpdateReferralUrl.url)
async def confirm_update_referral_url(message: Message, state: FSMContext):
    url = message.text
    await AdminService.update_referral_url(url)
    await state.clear()
    await message.answer(
        'Новая реферальная ссылка была установлена!\n'
        '❗️❗️❗️Не забудьте настроить постбеки для новой сссылки в лк 1win❗️❗️❗️',
        reply_markup=back_admin_kb)


# ================ #
@router.callback_query(F.data == 'update_support_url')
async def update_support_url(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateSupportUrl.url)
    await callback.message.edit_text(
        'Пришлите новую реф ссылку на саппорта',
        reply_markup=cancel_kb
    )


@router.message(UpdateSupportUrl.url)
async def confirm_update_support_url(message: Message, state: FSMContext):
    url = message.text
    await AdminService.update_support_url(url)
    await state.clear()
    await message.answer(
        'Новая ссылка на саппорта была установлена!\n',
        reply_markup=back_admin_kb)


# ================ #
@router.callback_query(F.data == 'update_faq')
async def update_faq(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Выберите раздел для которого вы хотите добавить вопрос',
        reply_markup=add_faq_kb
    )


@router.callback_query(F.data.startswith('add_faq_question_'))
async def add_faq_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data({
        'question_type': callback.data.split('_')[-1]
    })
    await callback.message.edit_text(
        text='Выберите язык для которого вы хотите добавить вопрос',
        reply_markup=select_faq_lang_kb
    )


@router.callback_query(F.data.startswith('select_faq_lang'))
async def select_faq_lang(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddFaqQuestion.question)
    await state.update_data({
        'question_lang': callback.data.split(':')[-1]
    })
    await callback.message.edit_text('Напишите вопрос для страницы, например:\n'
                                     'Как пользоваться компьютером?', reply_markup=cancel_kb)


@router.message(AddFaqQuestion.question)
async def add_faq_question_question(message: Message,
                                    state: FSMContext):
    question = message.text
    data = await state.get_data()
    question_type = data['question_type']

    res = await AdminService.check_question_available(
        question_type=question_type,
        question=question_type
    )
    if not res:
        await state.update_data({
            'question': question
        })
        await state.set_state(AddFaqAnswer.answer)
        await message.answer('Отлично! А теперь добавьте ответ на вопрос, например:\n'
                             'Для начала нужно подключить электро питание')
    else:
        await message.answer('Данный вопрос уже существует в этой категории! Попробуйте снова',
                             reply_markup=cancel_kb)


@router.message(AddFaqAnswer.answer)
async def add_faq_question_main_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    question = data['question']
    question_type = data['question_type']
    question_lang = data['question_lang']
    answer = message.text
    await AdminService.add_question(
        question=question,
        question_type=question_type,
        answer=answer,
        question_lang=question_lang
    )
    await state.clear()
    await message.answer('Вопрос успешно добавлен', reply_markup=back_admin_kb)


# ================ #
@router.callback_query(F.data == 'delete_faq')
async def delete_faq(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите раздел у которого вы хотите удалить вопрос',
        reply_markup=del_faq_kb
    )


@router.callback_query(F.data.startswith('del_faq_question_'))
async def delete_faq_answer(callback: CallbackQuery, ):
    await callback.message.edit_text(
        text='Выберите язык для которого вы хотите удалить вопрос',
        reply_markup=delete_faq_lang_kb(callback.data.split('_')[-1])
    )


@router.callback_query(F.data.startswith('del_faq_lang'))
async def del_faq_question_main_question(callback: CallbackQuery):
    faq_lang = callback.data.split(':')[1]
    faq_type = callback.data.split(':')[2]

    questions = await AdminService.get_faq(
        faq_types=faq_type,
        faq_lang=faq_lang
    )
    if questions:
        question = questions[0]
        await callback.message.edit_text(
            text='<b><i>Вопрос:</i></b>\n'
                 f'{question["question"]}\n\n'
                 f'<b><i>Ответ:</i></b>\n'
                 f'{question["answer"]}',
            parse_mode='HTML',
            reply_markup=faq_show(
                faq_id=question["id"],
                faq_type=faq_type,
                i=0,
                last_i=len(questions) - 1,
                faq_lang=faq_lang
            )
        )
    else:
        await callback.message.edit_text('Вопросы кончились!',
                                         reply_markup=back_admin_kb)


@router.callback_query(F.data.startswith('kill_faq_next'))
async def kill_faq_next(callback: CallbackQuery):
    data = callback.data.split(':')
    index = int(data[1])
    faq_lang = data[2]
    faq_type = data[3]
    questions = await AdminService.get_faq(
        faq_types=faq_type,
        faq_lang=faq_lang
    )

    question = questions[index]
    await callback.message.edit_text(
        text='<b><i>Вопрос:</i></b>\n'
             f'{question["question"]}\n\n'
             f'<b><i>Ответ:</i></b>\n'
             f'{question["answer"]}',
        parse_mode='HTML',
        reply_markup=faq_show(
            faq_id=question['id'],
            faq_type=faq_type,
            i=index,
            last_i=len(questions) - 1,
            faq_lang=faq_lang
        )
    )


@router.callback_query(F.data.startswith('kill_faq'))
async def kill_faq(callback: CallbackQuery):
    print(callback.data)
    question_id = int(callback.data.split(':')[1])
    await AdminService.del_question(question_id=question_id)
    await callback.message.edit_text('Вопрос удален!', reply_markup=back_admin_kb)


# ======== #
@router.callback_query(F.data == 'admin_list')
async def admin_list(callback: CallbackQuery):
    admins = await AdminService.get_admin_list()
    await callback.message.edit_text(
        text='АДМИНЫ',
        reply_markup=admin_list_kb(admins)
    )


@router.callback_query(F.data.startswith('del_admin'))
async def del_admin(callback: CallbackQuery):
    admin_id = callback.data.split(':')[-1]
    await AdminService.del_admin(int(admin_id))
    admins = await AdminService.get_admin_list()
    await callback.message.edit_text(
        text=f'Юзер с id = {admin_id} был удален из панели',
        reply_markup=admin_list_kb(admins)
    )


@router.callback_query(F.data == 'add_admin')
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddAdmin.admin_id)
    await callback.message.edit_text(
        text=f'Пришлите id админа для добавления',
        reply_markup=cancel_kb
    )


@router.message(AddAdmin.admin_id)
async def add_admin(message: Message, state: FSMContext):
    admin_id = message.text
    if admin_id.isdigit():
        await AdminService.add_admin(int(admin_id))
        await state.clear()
        await message.answer(f'Админ с id = {admin_id} успешно добавлен!',
                             reply_markup=back_admin_kb)
    else:
        await message.answer('ID должно быть числом! Попробуйте снова',
                             reply_markup=cancel_kb)


# ================ #