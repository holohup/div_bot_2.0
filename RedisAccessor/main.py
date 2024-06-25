import redis
from config import load_config, Config

c: Config = load_config()

r = redis.Redis(c.redis.host, c.redis.port)


r.set('aa', 'bb')
print(r.get('aa'))
