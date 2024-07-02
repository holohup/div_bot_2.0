import json
import logging

from dapr.aio.clients import DaprClient
from dapr.clients.grpc._response import InvokeMethodResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_instruments():
    async with DaprClient() as client:
        instruments: InvokeMethodResponse = await client.invoke_method(
            'tcs_api_accessor', 'get_instruments', ''
        )
    logger.debug(f"Got data: {instruments.json()}")
    return instruments.json()


async def request_prices(uids: list[str]):
    logger.info(f'Getting prices for {uids}')
    async with DaprClient() as client:
        prices: InvokeMethodResponse = await client.invoke_method(
            'tcs_api_accessor',
            'get_prices',
            data=json.dumps(uids),
            http_verb='POST'
        )
    logger.info(f'Got prices: {prices.json()}')
    return prices.json()
