import json
from abc import ABC, abstractmethod

from redis import Redis


class Storage(ABC):
    @abstractmethod
    def store(self, k: str, v: str):
        pass

    @abstractmethod
    def fetch_single_value(self, k: str):
        pass

    @abstractmethod
    def fetch_list_by_key(self, k: str):
        pass

    @abstractmethod
    def store_to_set(self, k, v):
        pass

    @abstractmethod
    def key_exists(self, k: str):
        pass

    @abstractmethod
    def drop_by_prefix(self, prefix: str):
        pass

    @abstractmethod
    def list_all_available_keys(self):
        pass


class RedisStorage(Storage):
    def __init__(self, r) -> None:
        self._r: Redis = r

    def store(self, k: str, v: str):
        self._r.set(k, json.dumps(v))

    def fetch_single_value(self, k: str):
        value = self._r.get(k)
        if value:
            return json.loads(str(value))
        return None

    def store_to_set(self, k: str, v: list):
        items = [json.dumps(item) for item in v]
        self._r.sadd(k, *items)

    def fetch_list_by_key(self, k: str):
        return self._r.smembers(k)

    def key_exists(self, k: str):
        return self._r.exists(k)

    def drop_by_prefix(self, prefix: str):
        for key in self._r.scan_iter(prefix + '*'):
            self._r.delete(key)

    def list_all_available_keys(self) -> list[str]:
        return self._r.keys('*')
