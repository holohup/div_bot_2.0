from typing import Literal, Optional
from pydantic import BaseModel
from datetime import datetime

class Instrument(BaseModel):
    ticker: str
    uid: str
    basic_asset: Optional[str] = None
    basic_asset_size: Optional[int] = None
    expiration_date: Optional[datetime] = None

class Instruments(BaseModel):
    instruments: list[Instrument]
