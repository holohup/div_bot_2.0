from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    token: str


@dataclass
class ServiceConfig:
    url: str

    @property
    def list(self) -> str:
        return self.url + '/list'

    def ticker(self, ticker: str) -> str:
        return self.url + '/ticker?ticker=' + ticker


@dataclass
class Config:
    bot: BotConfig
    service: ServiceConfig


def load_config():
    env = Env()
    env.read_env()
    DEBUG = str(env('DEBUG', False)).lower() in ('yes', 'true', '1', 'ok', 'debug')
    return Config(
        bot=BotConfig(token=env('TG_BOT_TOKEN')),
        service=ServiceConfig(
            url='http://localhost:8005' if DEBUG else 'http://prod:8005'
        ),
    )
