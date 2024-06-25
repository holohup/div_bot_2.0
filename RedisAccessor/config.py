from dataclasses import dataclass
import os


DEBUG = str(os.getenv('DEBUG', False)).lower() in ('true', 'yes', '1', 'on')
redis_host = 'localhost' if DEBUG else 'redis'


@dataclass
class RedisSettings:
    host: str
    port: int


@dataclass
class Config:
    redis: RedisSettings


def load_config(path: str = None) -> Config:
    return Config(
        redis=RedisSettings(host=redis_host, port=6379)
    )
