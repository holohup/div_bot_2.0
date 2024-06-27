from dataclasses import dataclass
import os
from datetime import timedelta

DEBUG = str(os.getenv('DEBUG', False)).lower() in ('true', '1', 'yes', 'on')


@dataclass
class ServiceConfig:
    address: str


@dataclass
class QueueConfig:
    pause_seconds: int


@dataclass
class Config:
    redis: ServiceConfig
    queue: QueueConfig


def load_config() -> Config:
    return Config(
        redis=ServiceConfig(
            address='localhost:50051' if DEBUG else 'redis_accessor:50051'
        ),
        queue=QueueConfig(pause_seconds=timedelta(seconds=10).seconds)
    )
