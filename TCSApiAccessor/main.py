import logging

from fastapi import FastAPI

from config import load_config
from schema import Instruments, Price
from tcs_api import TCSFetcher, get_last_prices

config = load_config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

fetcher = TCSFetcher(config.tcs)


@app.get('/get_instruments')
async def provide_instruments() -> Instruments:
    """Provides all available instruments."""

    if not config.tcs.token:
        return provide_fixture('instruments_response.json')
    return await fetcher.download_instruments()


@app.post('/get_prices')
async def get_latest_market_prices(uids: list[str]) -> list[Price]:
    """Gets a list of uids and returns the latest prices for the instruments."""

    if not config.tcs.token:
        fixtures = provide_fixture('prices_response.json')
        result = []
        for uid in uids:
            for fixture in fixtures:
                if fixture['uid'] != uid:
                    continue
                result.append(fixture)
        return result
    return await get_last_prices(uids, config.tcs)


def provide_fixture(filename: str):
    logger.info('Providing fixtures instead of real data')
    import json

    fixture_path = 'fixtures/' + filename
    with open(fixture_path, 'r') as file:
        json_data = json.load(file)
    return json_data


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
