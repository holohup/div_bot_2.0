from datetime import datetime

from pydantic import BaseModel


class Instrument(BaseModel):
    ticker: str
    uid: str


class Future(Instrument):
    basic_asset: str
    basic_asset_size: int
    expiration_date: datetime


class Stock(Instrument):
    pass


class Instruments(BaseModel):
    stocks: list[Stock]
    futures: list[Future]
