# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from proto import api_pb2 as proto_dot_api__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in proto/api_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class InstrumentsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveInstruments = channel.unary_unary(
                '/example.InstrumentsService/SaveInstruments',
                request_serializer=proto_dot_api__pb2.InstrumentsMessage.SerializeToString,
                response_deserializer=proto_dot_api__pb2.InstrumentsResponse.FromString,
                _registered_method=True)


class InstrumentsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SaveInstruments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InstrumentsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaveInstruments': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveInstruments,
                    request_deserializer=proto_dot_api__pb2.InstrumentsMessage.FromString,
                    response_serializer=proto_dot_api__pb2.InstrumentsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'example.InstrumentsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('example.InstrumentsService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class InstrumentsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SaveInstruments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/example.InstrumentsService/SaveInstruments',
            proto_dot_api__pb2.InstrumentsMessage.SerializeToString,
            proto_dot_api__pb2.InstrumentsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ListServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListRequest = channel.unary_unary(
                '/example.ListService/ListRequest',
                request_serializer=proto_dot_api__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_api__pb2.ListResponse.FromString,
                _registered_method=True)


class ListServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ListServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.ListRequest,
                    request_deserializer=proto_dot_api__pb2.Empty.FromString,
                    response_serializer=proto_dot_api__pb2.ListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'example.ListService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('example.ListService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ListService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/example.ListService/ListRequest',
            proto_dot_api__pb2.Empty.SerializeToString,
            proto_dot_api__pb2.ListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class TickerServiceStub(object):
    """Get a json of instruments for a ticker and a timestamp of the last db Updates

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TickerRequest = channel.unary_unary(
                '/example.TickerService/TickerRequest',
                request_serializer=proto_dot_api__pb2.GetTickerData.SerializeToString,
                response_deserializer=proto_dot_api__pb2.TickerResponse.FromString,
                _registered_method=True)


class TickerServiceServicer(object):
    """Get a json of instruments for a ticker and a timestamp of the last db Updates

    """

    def TickerRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TickerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TickerRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.TickerRequest,
                    request_deserializer=proto_dot_api__pb2.GetTickerData.FromString,
                    response_serializer=proto_dot_api__pb2.TickerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'example.TickerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('example.TickerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TickerService(object):
    """Get a json of instruments for a ticker and a timestamp of the last db Updates

    """

    @staticmethod
    def TickerRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/example.TickerService/TickerRequest',
            proto_dot_api__pb2.GetTickerData.SerializeToString,
            proto_dot_api__pb2.TickerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class RedisQueueStub(object):
    """Put and get messages to the queue
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PutMessage = channel.unary_unary(
                '/example.RedisQueue/PutMessage',
                request_serializer=proto_dot_api__pb2.MessageRequest.SerializeToString,
                response_deserializer=proto_dot_api__pb2.MessageResponse.FromString,
                _registered_method=True)
        self.GetMessage = channel.unary_unary(
                '/example.RedisQueue/GetMessage',
                request_serializer=proto_dot_api__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_api__pb2.MessageResponse.FromString,
                _registered_method=True)


class RedisQueueServicer(object):
    """Put and get messages to the queue
    """

    def PutMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RedisQueueServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PutMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.PutMessage,
                    request_deserializer=proto_dot_api__pb2.MessageRequest.FromString,
                    response_serializer=proto_dot_api__pb2.MessageResponse.SerializeToString,
            ),
            'GetMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMessage,
                    request_deserializer=proto_dot_api__pb2.Empty.FromString,
                    response_serializer=proto_dot_api__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'example.RedisQueue', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('example.RedisQueue', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RedisQueue(object):
    """Put and get messages to the queue
    """

    @staticmethod
    def PutMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/example.RedisQueue/PutMessage',
            proto_dot_api__pb2.MessageRequest.SerializeToString,
            proto_dot_api__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/example.RedisQueue/GetMessage',
            proto_dot_api__pb2.Empty.SerializeToString,
            proto_dot_api__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
