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
class Config:
    tcs: ServiceConfig
    redis: ServiceConfig
    db_update: DBUpdateConfig


def load_config() -> Config:
    return Config(
        tcs=ServiceConfig(
            address='http://localhost:8000' if DEBUG
            else 'http://tcs_api_accessor:8000'
        ),
        redis=ServiceConfig(
            address='localhost:50051' if DEBUG else 'redis:50051'
        ),
        db_update=DBUpdateConfig(timedelta(days=1)),
    )
