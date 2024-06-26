from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Instrument(BaseModel):
    ticker: str
    uid: str

class Future(Instrument):
    basic_asset: Optional[str]
    basic_asset_size: Optional[int]
    expiration_date: Optional[datetime]

class Stock(Instrument):
    pass

class Instruments(BaseModel):
    stocks: list[Stock]
    futures: list[Future]


class Price(BaseModel):
    uid: str
    price: Decimal

