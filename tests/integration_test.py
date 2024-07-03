# Theese are integration tests, will pass only with 'docker compose up'

import json
import os
import shutil
import time
from http import HTTPStatus

import pytest
import requests

URL = 'http://127.0.0.1:8005'
LIST_URL = URL + '/list'
TICKER_URL = lambda url: URL + '/ticker?ticker=' + url
LOG_CHECK_TIMEOUT_SECONDS: int = 60


@pytest.fixture
def log_file_backup():
    log_path = 'log.txt'
    backup_path = 'log.txt.bak'

    if os.path.exists(log_path):
        shutil.copy(log_path, backup_path)
    yield log_path

    if os.path.exists(backup_path):
        shutil.copy(backup_path, log_path)
        os.remove(backup_path)


def test_list_works():
    """
    The /list endpoint.
    In order for it to work, DivCounterManager, redis, RedisAccessor
    and TCSAPIAccessor should be up and running. gRPC and REST are
    tested too.
    """

    expected = (
        '"ABIO, AFKS, AFLT, ALRS, ASTR, BANE, BELU, BSPB, CBOM, CHMF, '
        "FEES, FESH, FLOT, GAZP, GMKN, HYDR, IRAO, KMAZ, LEAS, LKOH, "
        "MAGN, MGNT, MOEX, MTLR, MTSS, MVID, NLMK, NVTK, PHOR, PIKK, "
        "PLZL, POLY, POSI, RNFT, ROSN, RTKM, RUAL, SBER, SBERP, SGZH, "
        "SIBN, SMLT, SNGS, SNGSP, SOFL, SVCB, TATN, TATNP, TCSG, TRNFP, "
        'VKCO, WUSH"'
    )
    response = requests.get(LIST_URL)
    assert response.status_code == HTTPStatus.OK
    assert response.text == expected


def test_calculations_are_made():
    """
    Tests the functionality of the main modules works.
    Tests DivCounterManager, redis, RedisAccessor, TCSApiAccessor
    and the financial calculator within. Tests the gRPC and REST
    messaging between them.
    """

    expected_futures = ('SRU4', 'SRZ4', 'SRH5', 'SRM5')
    parsed_response = json.loads(requests.get(TICKER_URL("sber")).text)
    assert 'ticker' in parsed_response
    assert parsed_response['ticker'] == 'SBER'
    assert len(parsed_response) == 2
    assert 'dividends' in parsed_response
    futures_result = parsed_response['dividends']
    assert len(futures_result) == 4
    for i in range(len(expected_futures)):
        assert futures_result[i]['ticker'] == expected_futures[i]
        assert float(futures_result[i]['dividend']) >= 0


def test_logs_work(log_file_backup):
    """
    Tests that the logs work.
    For it to be true the Queue messanging service needs to work
    along with LogAccessor and gRPC.
    """

    log_file = log_file_backup
    expected_entry_1 = '| AKU4     | 20-09-24  |'
    expected_entry_2 = '| AKZ4     | 20-12-24  |'
    with open(log_file, 'r') as f:
        before_operations = f.read()
    requests.get(TICKER_URL("afks"))
    both_strings_found = False
    for pause in range(LOG_CHECK_TIMEOUT_SECONDS):
        with open(log_file, 'r') as f:
            after_operations = f.read()
        if (
            expected_entry_1 not in after_operations
            or expected_entry_2 not in after_operations
        ):
            time.sleep(1)
            continue
        both_strings_found = True
    assert before_operations != after_operations
    assert both_strings_found
