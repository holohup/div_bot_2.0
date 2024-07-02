import json
import logging
from datetime import datetime
from tabulate import tabulate

logger = logging.getLogger(__name__)

headers = ['Ticker', 'Expires', 'Dividend']


def format_log_message(msg: dict):
    ticker, futures = msg['ticker'], [json.loads(f) for f in msg['dividends']]
    logger.info(f'Preparing table for ticker {ticker}, {futures=}')
    table_data = [
        [
            f['ticker'],
            datetime.fromisoformat(f['expires']).strftime('%d-%m-%y'),
            f['dividend'],
        ]
        for f in futures
    ]
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    result = '\n' + ticker + '\n' + table + '\n' + '-' * 80
    return result
