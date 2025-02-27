from pydantic import BaseModel, Field

from enum import Enum

from typing import List


class FaqTypes(Enum):
    main = 'main'
    games = 'games'


class Faq(BaseModel):
    question: str
    answer: str


class FaqLang(Enum):
    ru = 'ru'
    uz = 'uz'
    hi = 'hi'
    en = 'en'


