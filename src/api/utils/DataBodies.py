# -*- coding: utf-8 -*-
import datetime

from pydantic import BaseModel

PATTERN = r'\p{IsCyrillic}'

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_TIME = "%Y-%m-%d %H:%M:%S"


class Subscribe(BaseModel):
    user_id: int
    gateway: int = None
    product_id: str
    transaction_id: str
    purchase_date_ms: datetime.datetime
    expires_date_ms: datetime.datetime
    status: int
    receipt: str = ''
    attempts: int = 0
