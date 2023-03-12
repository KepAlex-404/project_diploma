# -*- coding: utf-8 -*-
from pydantic import BaseModel

PATTERN = r'\p{IsCyrillic}'

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_TIME = "%Y-%m-%d %H:%M:%S"


class Subscribe(BaseModel):
    user_id: int
