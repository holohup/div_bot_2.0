from datetime import datetime
from pydantic import BaseModel


class FutureResult(BaseModel):
    ticker: str
    expires: datetime
    dividend: float


class Result(BaseModel):
    futures: list[FutureResult]
