from datetime import datetime
from decimal import Decimal

from schema import FutureResult


class FinancialCalculator:
    def __init__(self, discount_rate, tax):
        self._dr = discount_rate
        self._tax = tax

    def calculate(self, instruments):
        stock_price = self._get_decimal_price(instruments[0])
        result = []
        for future in instruments[1:]:
            result.append(self._get_future_result(future, stock_price))
        return result

    def _get_amount_of_days(self, future):
        return (
            datetime.fromisoformat(future['expiration_date']).date()
            - datetime.now().date()
        )

    def _calculate_dividends(
        self, stock_price, future_price, days, basic_asset_size
    ) -> float:
        daily_discount_rate = Decimal(self._dr) / Decimal('365') / 100
        present_value = future_price / (1 + daily_discount_rate) ** days
        dividend = stock_price - (present_value / basic_asset_size)
        return float(dividend / Decimal(str((100 - self._tax) / 100)))

    def _get_future_result(self, future, stock_price):
        future_price = self._get_decimal_price(future)
        days = int(self._get_amount_of_days(future).days)
        basic_asset_size = int(future['basic_asset_size'])
        div = round(
            self._calculate_dividends(
                stock_price, future_price, days, basic_asset_size
            ),
            2,
        )
        return FutureResult(
            ticker=future['ticker'],
            expires=datetime.date(datetime.fromisoformat(future['expiration_date'])),
            dividend=div,
        )

    def _get_decimal_price(self, instrument):
        return Decimal(instrument['price'])
