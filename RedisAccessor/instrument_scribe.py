import json
import logging
from pydantic.json import pydantic_encoder
from schema import Future, Stock

logger = logging.getLogger(__name__)


class InstrumentScribe:
    def __init__(self, storage, config) -> None:
        self._storage = storage
        self._config = config

    def save_instruments(self, instruments, timestamp: str):
        """The idea behind this is to store instruments by ticker.
        The same key (ticker) will store both the stock information
        and the futures list. So we are creating a dictionary which
        looks like:
        {ticker: {'stock': Stock, 'futures': [Future1, Future2, ..]}, ...}.
        The timestamp stores when the instruments were retrieved last
        in order to update cache when needed.
        """

        organized_by_ticker = self._organize_instruments(instruments)
        if len(organized_by_ticker) == 0:
            return
        self._storage.drop_by_prefix(prefix=self._config.storage.prefix)
        for ticker, instruments in organized_by_ticker.items():
            self._storage.store(
                ticker, json.dumps(instruments, default=pydantic_encoder)
            )
        logger.info(
            f'{len(organized_by_ticker.items())} tickers saved.'
        )
        self._storage.store(self._config.storage.timestamp_key, timestamp)
        logger.info(f'Timestamp updated: {timestamp}')

    def _organize_instruments(self, instruments):
        result = {}
        for instrument in instruments['futures']:
            ticker = self._config.storage.prefix + instrument['basic_asset']
            self._set_up_new_ticker(result, ticker)
            result[ticker]['futures'].append(Future(**instrument))
        for instrument in instruments['stocks']:
            ticker = self._config.storage.prefix + instrument['ticker']
            self._set_up_new_ticker(result, ticker)
            result[ticker]['stock'] = Stock(**instrument)
        return self._keep_only_tickers_with_pairs(result)

    def _keep_only_tickers_with_pairs(self, result):
        return {
            k: v for k, v in result.items() if (v['futures'] and v['stock'])
        }

    def _set_up_new_ticker(self, result, ticker):
        if ticker not in result.keys():
            result[ticker] = {'stock': None, 'futures': []}
        return ticker

    def _organize_futures(self, instruments):
        result = {}
        for instrument in instruments:
            ticker = instrument['basic_asset']
            if ticker not in result.keys():
                result[ticker] = []
            result[ticker].append(instrument)
        return result
