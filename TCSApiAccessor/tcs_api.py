import logging
from datetime import datetime, timedelta

from schema import Future, Instrument, Instruments, Price, Stock
from tinkoff.invest.retrying.aio.client import AsyncRetryingClient
from tinkoff.invest.schemas import Future as TFuture
from tinkoff.invest.schemas import Instrument as TCSInstrument
from tinkoff.invest.schemas import RealExchange
from tinkoff.invest.schemas import Share as TShare
from tinkoff.invest.utils import quotation_to_decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TCSFetcher:
    """Class to download and transform data.
    The public method is download_instruments()."""

    def __init__(self, config):
        self._token = config.token
        self._settings = config.settings
        logger.info(
            f'Init complete, token={self._obfuscate_token(self._token)}'
            f', {self._settings=}'
        )

    async def download_instruments(self) -> Instruments:
        futures_response: list[TFuture] = await self._fetch_data('futures')
        stocks_response: list[TShare] = await self._fetch_data('shares')
        futures = self._clean_and_transform_data(futures_response)
        stocks = self._clean_and_transform_data(stocks_response)
        return Instruments(stocks=stocks, futures=futures)

    async def _fetch_data(self, method: str) -> list[TCSInstrument]:
        logger.info(f'Downloading instruments for {method=}')
        async with AsyncRetryingClient(self._token, self._settings) as client:
            response = await getattr(client.instruments, method)()
        logger.info('Instrument download complete')
        return response.instruments

    def _clean_and_transform_data(
        self, instruments: list[TCSInstrument]
    ) -> list[Instrument]:
        result = []
        for instrument in instruments:
            if not instrument.real_exchange == RealExchange.REAL_EXCHANGE_MOEX:
                continue
            params = {'ticker': instrument.ticker, 'uid': instrument.uid}
            if isinstance(instrument, TShare):
                result.append(Stock(**params))
                continue

            if (
                not isinstance(instrument, TFuture)
                or instrument.expiration_date.date()
                <= datetime.now().date() + timedelta(days=3)
                or instrument.asset_type != 'TYPE_SECURITY'
                or int(quotation_to_decimal(instrument.basic_asset_size)) <= 0
            ):
                continue

            params.update(
                {
                    'basic_asset': instrument.basic_asset,
                    'basic_asset_size': int(
                        quotation_to_decimal(instrument.basic_asset_size)
                    ),
                    'expiration_date': instrument.expiration_date,
                }
            )
            result.append(Future(**params))
        logger.info('Instrument data preparation complete')
        return result

    @staticmethod
    def _obfuscate_token(token):
        if not token:
            return 'None'
        return ''.join(["*" if c != "." and c != "-" else c for c in token])


async def get_last_prices(uids: list[str], config) -> list[Price]:
    """Gets latest market prices for the uids."""

    logger.info(f'Getting last prices for {uids}')
    async with AsyncRetryingClient(config.token, settings=config.settings) as client:
        response = await client.market_data.get_last_prices(instrument_id=uids)
    result = [
        Price(uid=p.instrument_uid, price=quotation_to_decimal(p.price))
        for p in response.last_prices
    ]
    logger.info(f'result preparation complete: {result=}')
    return result
