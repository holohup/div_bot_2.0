from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal

from tinkoff.invest.retrying.aio.client import AsyncRetryingClient
from tinkoff.invest.schemas import InstrumentIdType as IdType
from tinkoff.invest.schemas import SecurityTradingStatus as TStatus
from tinkoff.invest.utils import quotation_to_decimal
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.schemas import FuturesResponse, SharesResponse, Instrument as TCSInstrument, RealExchange, Future

from schema import Instrument, Instruments


class TCSFetcher:
    def __init__(self, token: str, settings: RetryClientSettings):
        self._token = token
        self._settings = settings

    async def download_instruments(self):
        futures_response = await self._fetch_data('futures')
        stocks_response = await self._fetch_data('shares')
        futures = self._filter_fields(futures_response)
        stocks = self._filter_fields(stocks_response)
        print(len(futures), len(stocks))
        print(futures)

    async def _fetch_data(self, method: str) -> Instruments:
        async with AsyncRetryingClient(self._token, self._settings) as client:
            response: FuturesResponse = await getattr(client.instruments, method)()
        return response.instruments

    def _filter_fields(self, instruments: list[TCSInstrument]) -> Instruments:
        result = []
        for instrument in instruments:
            if not instrument.real_exchange == RealExchange.REAL_EXCHANGE_MOEX:
                continue
            params = {'ticker': instrument.ticker, 'uid': instrument.uid}
            if (
                isinstance(instrument, Future)
                and instrument.expiration_date.date() > datetime.now().date() + timedelta(days=3)
                and instrument.asset_type == 'TYPE_SECURITY'
            ):
                params.update({
                    'basic_asset': instrument.basic_asset,
                    'basic_asset_size': int(quotation_to_decimal(instrument.basic_asset_size)),
                    'expiration_date': instrument.expiration_date
                })
            result.append(Instrument(**params))
        return result

# async def fetch_stocks() -> pd.DataFrame:
#     async with AsyncRetryingClient(TCS_RO_TOKEN, settings=RETRY_SETTINGS) as client:
#         response = await client.instruments.shares()
#         return pd.DataFrame(response.instruments)


# async def is_trading_now(future: pd.Series):
#     async with AsyncRetryingClient(TCS_RO_TOKEN, settings=RETRY_SETTINGS) as client:
#         response = await client.instruments.future_by(
#             id_type=IdType.INSTRUMENT_ID_TYPE_UID, id=future["uid"]
#         )
#     return (
#         response.instrument.trading_status
#         == TStatus.SECURITY_TRADING_STATUS_NORMAL_TRADING
#     )


# async def get_last_prices(uids: pd.Series) -> list[Decimal]:
#     async with AsyncRetryingClient(TCS_RO_TOKEN, settings=RETRY_SETTINGS) as client:
#         response = await client.market_data.get_last_prices(
#             instrument_id=uids.to_list()
#         )
#         result = [quotation_to_decimal(p.price) for p in response.last_prices]
#         return result
