import os
from dataclasses import dataclass
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
class PubSubConfig:
    channel_name: str
    pubsub_name: str


@dataclass
class Config:
    redis: ServiceConfig
    db_update: DBUpdateConfig
    finance: FinancialConfig
    pubsub: PubSubConfig


def load_config() -> Config:
    return Config(
        redis=ServiceConfig(
            address='localhost:50051' if DEBUG else 'redis_accessor:50051'
        ),
        db_update=DBUpdateConfig(timedelta(days=1)),
        finance=FinancialConfig(discount_rate=16.0, tax=13.0),
        pubsub=PubSubConfig(channel_name='queries', pubsub_name='logpubsub'),
    )
