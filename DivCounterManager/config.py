from dataclasses import dataclass
import os
from datetime import timedelta

DEBUG = str(os.getenv('DEBUG', False)).lower() in ('true', '1', 'yes', 'on')


@dataclass
class ServiceConfig:
    address: str


@dataclass
class DBUpdateConfig:
    pause_between_updates: timedelta


@dataclass
class FinancialConfig:
    discount_rate: float
    tax: float


@dataclass
class Config:
    tcs: ServiceConfig
    redis: ServiceConfig
    db_update: DBUpdateConfig
    finance: FinancialConfig


def load_config() -> Config:
    return Config(
        tcs=ServiceConfig(
            address='http://localhost:8000' if DEBUG
            else 'http://tcs_api_accessor:8000'
        ),
        redis=ServiceConfig(
            address='localhost:50051' if DEBUG else 'redis_accessor:50051'
        ),
        db_update=DBUpdateConfig(timedelta(days=1)),
        finance=FinancialConfig(discount_rate=16.0, tax=13.0)
    )
