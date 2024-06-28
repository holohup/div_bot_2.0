# Theese are integration tests, will pass only with 'docker compose up'

import requests
from http import HTTPStatus
import time
import pytest
import os
import shutil

URL = "http://127.0.0.1:8005"
LIST_URL = URL + "/list"
TICKER_URL = lambda url: URL + "/ticker?ticker=" + url


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


def test_calculations_are_correct():
    """
    Tests the functionality of the main modules works.
    Tests DivCounterManager, redis, RedisAccessor, TCSApiAccessor
    and the financial calculator within. Tests the gRPC and REST
    messaging between them.
    """

    expected = (
        '{"ticker":"SBER",'
        '"dividends":[{"ticker":"SRU4","expires":"2024-09-20T00:00:00",'
        '"dividend":32.06},{"ticker":"SRZ4","expires":"2024-12-20T00:00:00"'
        ',"dividend":32.93},{"ticker":"SRH5","expires":"2025-03-21T00:00:00"'
        ',"dividend":29.08},{"ticker":"SRM5","expires":"2025-06-20T00:00:00"'
        ',"dividend":40.77}]}'
    )
    response = requests.get(TICKER_URL("sber"))
    assert response.text == expected


def test_logs_work(log_file_backup):
    """
    Tests that the logs work.
    For it to be true the Queue messanging service needs to work
    along with LogAccessor and gRPC.
    """

    log_file = log_file_backup
    expected_entry = (
        'AFKS' + '\n'
        '+----------+-----------+------------+' + '\n'
        '| Ticker   | Expires   |   Dividend |' + '\n'
        '+==========+===========+============+' + '\n'
        '| AKU4     | 20-09-24  |       0.64 |' + '\n'
        '+----------+-----------+------------+' + '\n'
        '| AKZ4     | 20-12-24  |       1.22 |' + '\n'
        '+----------+-----------+------------+'
    )
    with open(log_file, 'r') as f:
        before_operations = f.read()
    requests.get(TICKER_URL("afks"))
    time.sleep(60)
    with open(log_file, 'r') as f:
        after_operations = f.read()
    assert before_operations != after_operations
    assert expected_entry in after_operations
