import os
from dataclasses import dataclass

DEBUG = str(os.getenv('DEBUG', False)).lower() in ('true', 'yes', '1', 'on')
redis_host = 'localhost' if DEBUG else 'redis'


@dataclass
class RedisSettings:
    host: str
    port: int


@dataclass
class GRPCSettings:
    address: str


@dataclass
class StorageSettings:
    prefix: str
    timestamp_key: str


@dataclass
class ChannelSettings:
    name: str


@dataclass
class Config:
    redis: RedisSettings
    grpc: GRPCSettings
    storage: StorageSettings
    channel: ChannelSettings


def load_config(path: str = '') -> Config:
    return Config(
        redis=RedisSettings(host=redis_host, port=6379),
        grpc=GRPCSettings(address='[::]:50051'),
        storage=StorageSettings(prefix='TICKER:', timestamp_key='timestamp'),
        channel=ChannelSettings(name='lists')
    )
