import json
import logging


from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
import redis


from config import Config, load_config
from instrument_scribe import InstrumentScribe
from storage import RedisStorage, Storage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config: Config = load_config()

r = redis.Redis(config.redis.host, config.redis.port, decode_responses=True)
storage: Storage = RedisStorage(r)


app = App()


@app.method(name='save_instruments')
def store_instruments(request: InvokeMethodRequest) -> InvokeMethodResponse:
    logger.info('Received save instruments request.')
    request = json.loads(request.text())
    try:
        instruments = request['instruments']
        timestamp = request['timestamp']
        logger.info(
            'Trying to save instruments,' f' timestamp = {request["timestamp"]}'
        )
        scribe = InstrumentScribe(storage, config)
        scribe.save_instruments(json.loads(instruments), timestamp)
        response = InvokeMethodResponse(data='ok', status_code=200)
    except Exception as e:
        response = InvokeMethodResponse(data=f'Error: {e}', status_code=500)
    return response


@app.method(name='list_tickers')
def list_available_tickers(request) -> InvokeMethodResponse:
    tickers_with_prefix = storage.list_all_available_keys()
    prefix = config.storage.prefix
    result = [t.partition(prefix)[-1] for t in tickers_with_prefix if prefix in t]
    return InvokeMethodResponse(', '.join(sorted(result)), status_code=200)


@app.method(name='get_instruments_by_ticker')
def get_instruments_by_ticker(request: InvokeMethodRequest) -> InvokeMethodResponse:
    ts = (
        storage.fetch_single_value(config.storage.timestamp_key)
        if storage.key_exists(config.storage.timestamp_key)
        else '1970-01-01T00:00:00Z'
    )
    response = {
        'timestamp': ts,
        'data': storage.fetch_single_value(
            config.storage.prefix + request.text().upper()
        ),
    }

    logger.info(f'Returning ticker info and timestamp: {response}')
    return InvokeMethodResponse(data=json.dumps(response), status_code=200)


if __name__ == '__main__':
    print('starting')
    app.run(50051)
