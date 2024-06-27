from proto.api_pb2_grpc import RedisQueueServicer
from proto.api_pb2 import MessageResponse


class RedisQueueAccessor(RedisQueueServicer):
    def __init__(self, r, queue_name: str):
        self._r = r
        self._name = queue_name

    def PutMessage(self, request, context):
        self._r.rpush(self._name, request.message)
        return MessageResponse(message="Message added to queue")

    def GetMessage(self, request, context):
        message = self._r.lpop(self._name)
        if message:
            return MessageResponse(message=message)
        else:
            return MessageResponse(message='')
