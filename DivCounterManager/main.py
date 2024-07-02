import grpc
from fastapi import FastAPI
import uvicorn
from config import load_config
import json
from contextlib import asynccontextmanager
import logging
from financial_calculator import FinancialCalculator
from utils import (
    get_instruments_by_ticker, fill_instruments_with_prices,
    prepare_instruments, prepare_prices, fetch_tickers_from_db,
    send_message_to_log_calculation
)
from publisher import publish_log_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


config = load_config()
fin_calc = FinancialCalculator(
    config.finance.discount_rate, config.finance.tax
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    channel = grpc.aio.insecure_channel(config.redis.address)
    await get_instruments_by_ticker('', channel, config)
    app.state.channel = channel
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/ticker')
async def count_dividends(ticker: str):
    matching_instruments = await get_instruments_by_ticker(
        ticker, app.state.channel, config
    )
    if not matching_instruments:
        return {
            'result':
            f'Instrument with futures not found for ticker {ticker.upper()}'
        }
    instruments = prepare_instruments(json.loads(matching_instruments))
    prices_json = await prepare_prices(instruments)
    fill_instruments_with_prices(instruments, prices_json)
    result = fin_calc.calculate(instruments)
    log_result = {
        'ticker': ticker.upper(),
        'dividends': [str(r.json()) for r in result]
    }
    await publish_log_message(json.dumps(log_result), config.pubsub)
    return {
        'ticker': ticker.upper(), 'dividends': result
    }


@app.get('/list')
async def get_tickers_list():
    list_response = await fetch_tickers_from_db(app.state.channel)
    return list_response


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8005, reload=True)
