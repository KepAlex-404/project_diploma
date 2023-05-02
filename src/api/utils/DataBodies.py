# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel, conint

PATTERN = r'\p{IsCyrillic}'

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_TIME = "%Y-%m-%d %H:%M:%S"


class Subscribe(BaseModel):
    user_id: int


class Meta(BaseModel):
    # todo add stopwords
    header: bool = True
    delimiter: str = ","
    column: Optional[str] = 'text'
    topics_num: conint(ge=5, le=20) = 10
    stop_words: Optional[List[str]]


class AnalyserBody(BaseModel):
    model_id: str
    text: Optional[str]
