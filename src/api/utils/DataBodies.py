# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel, conint

PATTERN = r'\p{IsCyrillic}'

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_TIME = "%Y-%m-%d %H:%M:%S"


class Subscribe(BaseModel):
    user_id: int


class Meta(BaseModel):
    header: bool = True
    delimiter: str = ","
    column: Optional[str] = 'text'
    topics_num: conint(ge=5, le=20) = 10
    stop_words: Optional[List[str]]


class AnalyserBody(BaseModel):
    model_id: str
    text: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str