from fastapi import FastAPI, Request
import logging

from config import load_config
from log_formatter import format_log_message

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = load_config()


@app.get('/dapr/subscribe')
async def subscribe():
    return [{
        'pubsubname': config.pubsub.pubsub_name,
        'topic': config.pubsub.channel_name,
        'route': config.pubsub.channel_name
    }]


@app.post(f'/{config.pubsub.channel_name}')
async def log_query_handler(request: Request):
    event = await request.json()
    logger.info(f"Received event: {event}")
    result = format_log_message(event['data'])
    with open('log.txt', '+a') as file:
        file.write(result)
    logger.info('log.txt update complete')
    return {"status": "SUCCESS"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8001)
