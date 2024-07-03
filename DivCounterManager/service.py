import json
import logging
from datetime import UTC, datetime

from grpc_requests import get_ticker_data, list_tickers, save_instruments
from http_requests import get_all_instruments, request_prices

logger = logging.getLogger(__name__)


async def get_instruments_by_ticker(ticker, pause):
    logger.info(f'Getting ticker {ticker} from DAPR service')
    response = await get_ticker_data(ticker)
    logger.info(f'Received data from DAPR: {response}')
    now = datetime.now(UTC)
    if now - datetime.fromisoformat(json.loads(response)['timestamp']) > pause:
        logger.info('Updating tickers db from dapr')
        instruments = await get_all_instruments()
        logger.debug(f'Received instruments: {instruments}')
        result = await update_instruments(json.dumps(instruments))
        logger.info(f'Updated instruments, {result=}')
        if result != 'ok':
            logger.error('Error updating instruments')
        else:
            logger.info('DB updated')
    return json.loads(response)['data']


async def update_instruments(instruments: str) -> str:
    return await save_instruments(instruments, datetime.now(UTC).isoformat())


def prepare_instruments(i_json):
    instruments = [i_json['stock']]
    instruments.extend(sorted(i_json['futures'], key=lambda a: a['expiration_date']))
    return instruments


def fill_instruments_with_prices(instruments, p_json):
    for i in range(len(instruments)):
        if instruments[i]['uid'] != p_json[i]['uid']:
            string = (
                'Something is not right in the ordering of items'
                f'Instruments = {instruments}, p_json = {p_json}'
            )
            logger.error(string)
            raise ValueError(string)
        instruments[i]['price'] = p_json[i]['price']


async def prepare_prices(instruments):
    return await request_prices([i['uid'] for i in instruments])


async def fetch_tickers_from_db():
    return await list_tickers()
