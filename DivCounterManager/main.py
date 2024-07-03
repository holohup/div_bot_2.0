import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from config import load_config
from financial_calculator import FinancialCalculator
from publisher import publish_log_message
from service import (
    fetch_tickers_from_db,
    fill_instruments_with_prices,
    get_instruments_by_ticker,
    prepare_instruments,
    prepare_prices,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


config = load_config()
fin_calc = FinancialCalculator(config.finance.discount_rate, config.finance.tax)


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_ready = False
    while not grpc_ready:
        try:
            await get_instruments_by_ticker('', config.db_update.pause_between_updates)
        except Exception as e:
            logger.warning(str(e))
            await asyncio.sleep(1)
        else:
            grpc_ready = True
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/ticker')
async def count_dividends(ticker: str):
    matching_instruments = await get_instruments_by_ticker(
        ticker, config.db_update.pause_between_updates
    )
    if not matching_instruments:
        return {
            'result': f'Instrument with futures not found for ticker {ticker.upper()}'
        }
    instruments = prepare_instruments(json.loads(matching_instruments))
    prices_json = await prepare_prices(instruments)
    fill_instruments_with_prices(instruments, prices_json)
    result = fin_calc.calculate(instruments)
    log_result = {
        'ticker': ticker.upper(),
        'dividends': [str(r.json()) for r in result],
    }
    await publish_log_message(json.dumps(log_result), config.pubsub)
    return {'ticker': ticker.upper(), 'dividends': result}


@app.get('/list')
async def get_tickers_list():
    list_response = await fetch_tickers_from_db()
    return list_response


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8005)
