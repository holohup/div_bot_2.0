import json
from config import Config, load_config
from concurrent import futures
import grpc
from proto import api_pb2
from proto import api_pb2_grpc
import redis
from schema import Future, Stock
from storage import RedisStorage, Storage
from pydantic.json import pydantic_encoder
from google.protobuf.timestamp_pb2 import Timestamp
from queue_accessor import RedisQueueAccessor

config: Config = load_config()

r = redis.Redis(config.redis.host, config.redis.port, decode_responses=True)
storage = RedisStorage(r)


class InstrumentScribe:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def save_instruments(self, instruments, timestamp):
        """The idea behind this is to store instruments by ticker.
        The same key (ticker) will store both the stock information
        and the futures list. So we are creating a dictionary which
        looks like:
        {ticker: {'stock': Stock, 'futures': [Future1, Future2, ..]}, ...}.
        """

        organized_by_ticker = self._organize_instruments(instruments)
        if len(organized_by_ticker) == 0:
            return
        self._storage.drop_by_prefix(prefix=config.storage.prefix)
        for ticker, instruments in organized_by_ticker.items():
            self._storage.store(
                ticker, json.dumps(instruments, default=pydantic_encoder)
            )
        self._storage.store(config.storage.timestamp_key, timestamp)

    def _organize_instruments(self, instruments):
        result = {}
        for instrument in instruments['futures']:
            ticker = config.storage.prefix + instrument['basic_asset']
            self._set_up_new_ticker(result, ticker)
            result[ticker]['futures'].append(Future(**instrument))
        for instrument in instruments['stocks']:
            ticker = config.storage.prefix + instrument['ticker']
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


class InstrumentsServiceServicer(api_pb2_grpc.InstrumentsServiceServicer):
    def SaveInstruments(self, request, context):
        response = api_pb2.InstrumentsResponse()
        try:
            instruments = json.loads(request.message)
            timestamp = request.timestamp
            scribe = InstrumentScribe(storage)
            scribe.save_instruments(instruments, timestamp.ToJsonString())
            response.message = 'ok'
        except Exception as e:
            response.message = str(e)
        return response


class ListServiceServicer(api_pb2_grpc.ListServiceServicer):
    def ListRequest(self, request, context):
        response = ', '.join(sorted(prepare_tickers_list()))
        return api_pb2.ListResponse(message=response)


class TickerServiceServicer(api_pb2_grpc.TickerServiceServicer):
    def TickerRequest(self, request, context):
        timestamp = Timestamp()
        ts = (
            storage.fetch_single_value(config.storage.timestamp_key)
            if storage.key_exists(config.storage.timestamp_key)
            else '1970-01-01T00:00:00Z'
        )
        timestamp.FromJsonString(ts)
        response = api_pb2.TickerResponse(
            timestamp=timestamp,
            message=storage.fetch_single_value(
                config.storage.prefix + request.message.upper()
            ),
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_InstrumentsServiceServicer_to_server(
        InstrumentsServiceServicer(), server
    )
    api_pb2_grpc.add_ListServiceServicer_to_server(
        ListServiceServicer(), server
    )
    api_pb2_grpc.add_TickerServiceServicer_to_server(
        TickerServiceServicer(), server
    )
    api_pb2_grpc.add_RedisQueueServicer_to_server(
        RedisQueueAccessor(r, config.channel.name), server
    )

    server.add_insecure_port(config.grpc.address)
    server.start()
    server.wait_for_termination()


def prepare_tickers_list():
    tickers_with_prefix = storage.list_all_available_keys()
    prefix = config.storage.prefix
    result = [
        t.partition(prefix)[-1] for t in tickers_with_prefix if prefix in t
    ]
    return result


if __name__ == '__main__':
    serve()
