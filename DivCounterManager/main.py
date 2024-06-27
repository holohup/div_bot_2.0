import asyncio
import grpc
from fastapi import FastAPI
from config import load_config
import json
import logging
from financial_calculator import FinancialCalculator
from utils import (
    get_instruments_by_ticker, fill_instruments_with_prices,
    prepare_instruments, prepare_prices, fetch_tickers_from_db,
    send_message_to_log_calculation
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
config = load_config()
channel = grpc.aio.insecure_channel(config.redis.address)
fin_calc = FinancialCalculator(
    config.finance.discount_rate, config.finance.tax
)


@app.get('/ticker')
async def count_dividends(ticker: str):
    matching_instruments = await get_instruments_by_ticker(
        ticker, channel, config
    )
    if not matching_instruments:
        return {
            'result':
            f'Instrument with futures not found for ticker {ticker.upper()}'
        }
    instruments = prepare_instruments(json.loads(matching_instruments))
    prices_json = await prepare_prices(instruments, config)
    fill_instruments_with_prices(instruments, prices_json)
    result = fin_calc.calculate(instruments)
    await send_message_to_log_calculation(channel, ticker, result)
    return {
        'ticker': ticker.upper(), 'dividends': result
    }


@app.get('/list')
async def get_tickers_list():
    list_response = await fetch_tickers_from_db(channel)
    return list_response


@app.on_event('startup')
async def startup():
    asyncio.create_task(get_instruments_by_ticker('', channel, config))
