import grpc
from proto import api_pb2_grpc, api_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import FastAPI
import httpx
from config import load_config
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
config = load_config()
channel = grpc.aio.insecure_channel(config.redis.address)

def dt_from_ts(ts: Timestamp) -> datetime:
    return datetime.fromtimestamp(ts.seconds + ts.nanos/1e9)


@app.get('/')
async def check_async():
    instruments = await refresh_instruments()
    result = await update_instruments(instruments)
    if result != 'ok':
        logger.error('Error updating instruments')
    return result


@app.get('/ticker')
async def count_dividends(ticker: str):
    matching_instruments = await get_instruments_by_ticker(ticker)
    if not matching_instruments:
        return {
            'result': f'not found any instruments with futures for ticker {ticker.upper()}'
        }
    i_json = json.loads(matching_instruments)
    instruments = [i_json['stock']]
    instruments.extend(sorted(i_json['futures'], key=lambda a: a['expiration_date']))
    uids = [instrument['uid'] for instrument in instruments]
    prices = await get_last_prices(uids)
    p_json = json.loads(prices)
    for i in range(len(instruments)):
        if instruments[i]['uid'] != p_json[i]['uid']:
            string = (
                'Something is not right in the ordering of items'
                f'Instruments = {instruments}, p_json = {p_json}'
            )
            logger.error(string)
            raise ValueError(string)
        instruments[i]['price'] = p_json[i]['price']
    return 


async def get_instruments_by_ticker(ticker):
    ticker_stub = api_pb2_grpc.TickerServiceStub(channel)
    ticker_response = await ticker_stub.TickerRequest(
        api_pb2.GetTickerData(message=ticker)
    )
    current_time = Timestamp()
    current_time.FromDatetime(datetime.now())
    if (dt_from_ts(current_time) - dt_from_ts(ticker_response.timestamp)
        > config.db_update.pause_between_updates
    ):
        logger.info('Updating tickers db')
        instruments = await refresh_instruments()
        result = await update_instruments(instruments)
        if result != 'ok':
            logger.error('Error updating instruments')
        else:
            logger.info('DB updated')
    return ticker_response.message


async def update_instruments(instruments: str):
    stub = api_pb2_grpc.InstrumentsServiceStub(channel)
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime.now())
    request = api_pb2.InstrumentsMessage(timestamp=timestamp, message=instruments)
    response: api_pb2.InstrumentsResponse = await stub.SaveInstruments(request)
    return response.message


async def refresh_instruments():
    async with httpx.AsyncClient() as client:
        result = await client.get(config.tcs.address + '/get_instruments')
    return result.text


async def get_last_prices(uids: list[str]):
    async with httpx.AsyncClient() as client:
        response = await client.post(config.tcs.address + '/get_prices', json=uids)
    return response.text
