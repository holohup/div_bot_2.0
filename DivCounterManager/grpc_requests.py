import json
import logging

from dapr.aio.clients import DaprClient
from dapr.clients.grpc._response import InvokeMethodResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def save_instruments(instruments: str, timestamp: str):
    logger.info('Saving instruments.')
    logger.debug(f'{instruments=}')
    data = {'instruments': instruments, 'timestamp': timestamp}
    async with DaprClient() as client:
        result: InvokeMethodResponse = await client.invoke_method(
            'redis_accessor', 'save_instruments', json.dumps(data)
        )
    txt = result.text()
    if txt != 'ok':
        logger.error(f'Error saving instruments: {txt}')
    logger.info('Saved successfully.')
    return txt


async def list_tickers():
    logger.info('Preparing tickers list')
    async with DaprClient() as client:
        result: InvokeMethodResponse = await client.invoke_method(
            'redis_accessor', 'list_tickers', ''
        )
    txt = result.text()
    if result.status_code != 200:
        logger.error(f'Error retrieving tickers: {txt}')
        return txt
    logger.info(f'Retrieved successfully.{txt}')
    return txt


async def get_ticker_data(ticker: str):
    async with DaprClient() as client:
        result: InvokeMethodResponse = await client.invoke_method(
            'redis_accessor', 'get_instruments_by_ticker', ticker
        )
    txt = result.text()
    if result.status_code != 200:
        logger.error(f'Error retrieving ticker data: {txt}')
        return txt
    logger.info(f'Retrieved successfully. {txt}')
    return txt
