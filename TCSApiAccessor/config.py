import os
from dataclasses import dataclass
from tinkoff.invest.retrying.settings import RetryClientSettings


@dataclass
class TCSConfig:
    token: str
    settings: RetryClientSettings


@dataclass
class Config:
    tcs: TCSConfig


def load_config():
    return Config(
        tcs=TCSConfig(
            token=os.getenv("TCS_RO_TOKEN"),
            settings=RetryClientSettings(use_retry=True, max_retry_attempt=100),
        ),
    )
