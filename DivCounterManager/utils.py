import json
from google.protobuf.timestamp_pb2 import Timestamp
from proto.api_pb2_grpc import (
    RedisQueueStub, TickerServiceStub, InstrumentsServiceStub, ListServiceStub
)
from proto.api_pb2 import (
    MessageRequest, GetTickerData, InstrumentsMessage, Empty
)
from datetime import datetime
from http_requests import http_get, http_post
import logging

logger = logging.getLogger(__name__)


async def put_message_in_queue(channel, message: str):
    queue_stub = RedisQueueStub(channel)
    await queue_stub.PutMessage(MessageRequest(message=message))


def dt_from_ts(ts: Timestamp) -> datetime:
    return datetime.fromtimestamp(ts.seconds + ts.nanos/1e9)


async def get_instruments_by_ticker(ticker, channel, config):
    ticker_stub = TickerServiceStub(channel)
    logger.info(f'Getting ticker {ticker} from TickerService')
    ticker_response = await ticker_stub.TickerRequest(
        GetTickerData(message=ticker)
    )
    logger.info('Received data from TickerService')
    current_time = Timestamp()
    current_time.FromDatetime(datetime.now())
    if (
        dt_from_ts(current_time) - dt_from_ts(ticker_response.timestamp)
        > config.db_update.pause_between_updates
    ):
        logger.info(
            f'Updating tickers db from {config.tcs.address + "/get_instruments"}'
        )
        instruments = await http_get(config.tcs.address + '/get_instruments')
        logger.info(f'Received instruments: {instruments}')
        result = await update_instruments(instruments, channel)
        logger.info(f'Updated instruments, {result=}')
        if result != 'ok':
            logger.error('Error updating instruments')
        else:
            logger.info('DB updated')
    return ticker_response.message


async def update_instruments(instruments: str, channel):
    stub = InstrumentsServiceStub(channel)
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime.now())
    request = InstrumentsMessage(
        timestamp=timestamp, message=instruments
    )
    response = await stub.SaveInstruments(request)
    return response.message


def prepare_instruments(i_json):
    instruments = [i_json['stock']]
    instruments.extend(
        sorted(i_json['futures'], key=lambda a: a['expiration_date'])
    )
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


async def prepare_prices(instruments, config):
    prices = await http_post(
        config.tcs.address + '/get_prices',
        [instrument['uid'] for instrument in instruments]
    )
    return json.loads(prices)


async def fetch_tickers_from_db(channel):
    list_stub = ListServiceStub(channel)
    list_response = await list_stub.ListRequest(Empty())
    return list_response.message


async def send_message_to_log_calculation(channel, ticker: str, result):
    message = (
        ticker.upper() + '***'
        + '@@@'.join([r.model_dump_json() for r in result])
    )
    await put_message_in_queue(channel, message)
