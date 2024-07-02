from dataclasses import dataclass
import os


@dataclass
class PubSubConfig:
    channel_name: str
    pubsub_name: str


@dataclass
class Config:
    pubsub: PubSubConfig


def load_config() -> Config:
    return Config(
        pubsub=PubSubConfig(channel_name='queries', pubsub_name='logpubsub')
    )
