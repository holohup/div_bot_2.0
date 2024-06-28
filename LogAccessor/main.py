import asyncio
from datetime import datetime
import json
from proto.api_pb2_grpc import RedisQueueStub
from proto.api_pb2 import Empty
import logging
from config import load_config
import grpc
from tabulate import tabulate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = load_config()

headers = ['Ticker', 'Expires', 'Dividend']


async def periodically_check_queue(pause_seconds: int = 10):
    channel = grpc.aio.insecure_channel(config.redis.address)
    queue_stub = RedisQueueStub(channel)

    while True:
        message = await queue_stub.GetMessage(Empty())
        if message.message:
            log_calculations(message.message)
        await asyncio.sleep(pause_seconds)


def log_calculations(msg: str):
    ticker, futures = msg.split('***')
    futures = [json.loads(f) for f in futures.split('@@@')]
    table_data = [
        [
            f['ticker'],
            datetime.fromisoformat(f['expires']).strftime('%d-%m-%y'),
            f['dividend'],
        ]
        for f in futures
    ]
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    result = '\n' + ticker + '\n' + table + '\n' + '-' * 80
    with open('log.txt', '+a') as file:
        file.write(result)


async def main():
    await periodically_check_queue(config.queue.pause_seconds)


if __name__ == "__main__":
    asyncio.run(main())
