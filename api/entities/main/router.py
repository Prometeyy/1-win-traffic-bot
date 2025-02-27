from fastapi import APIRouter, Header

from typing import List

from entities.main.service import MainService

from entities.main.dto import FaqTypes, Faq, FaqLang

router = APIRouter(
    prefix='',
    tags=['Main']
)


@router.get('/lucky-jet',
            response_model=float)
async def get_lucky_jet(
):
    return await MainService.get_lucky_get_signal()


@router.get('/mines/{mines}',
            response_model=List[List[bool]],
            description='Возращает матрицу 5*5 где полу True = мине. Всего полей True будет mines штук\n\n'
                        '^кол-во мин (mines) передается в пути запроса')
async def get_1win_mines(
        mines: int,
):
    return MainService.get_mines_signal(mines)


@router.get('/faq/{lang}/{faq_type}',
            response_model=List[Faq],
            description='Список может быть пустым')
async def get_faq(
        lang: FaqLang,
        faq_type: FaqTypes,
):
    return await MainService.get_faq(
        faq_types=faq_type,
        faq_lang=lang
    )


@router.get('/support',
            description='Ссылка на акк. поддержки',
            response_model=str)
async def get_support():
    return await MainService.get_support()


@router.get('/referral',
            description='Ссылка на партнерскую ссылку 1win',
            response_model=str)
async def get_partner():
    return await MainService.get_referral()
