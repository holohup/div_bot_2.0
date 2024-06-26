import pickle
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tcs_api import TCSFetcher


@dataclass
class DummyConfig:
    token: str = ''
    settings: str = ''

def load_fixture(filename: str):
    fixture_path = Path(__file__).parent / 'fixtures' / filename
    with open(fixture_path, 'rb') as f:
        loaded_instruments = pickle.load(f)
    return loaded_instruments

def test_futures_filters():
    loaded_instruments = load_fixture('futures.pkl')
    assert len(loaded_instruments) == 345
    filtered = TCSFetcher(DummyConfig())._clean_and_transform_data(loaded_instruments)
    assert len(filtered) == 148
    for instrument in filtered:
        assert instrument.expiration_date > datetime(year=2024, month=6, day=26).replace(tzinfo=timezone.utc) + timedelta(days=3)
        assert isinstance(instrument.basic_asset, str)
        assert isinstance(instrument.basic_asset_size, int)
        assert instrument.basic_asset_size > 0


def test_stocks_filters():
    loaded_instruments = load_fixture('stocks.pkl')
    assert len(loaded_instruments) == 1998
    filtered = TCSFetcher(DummyConfig())._clean_and_transform_data(loaded_instruments)
    assert len(filtered) == 167
