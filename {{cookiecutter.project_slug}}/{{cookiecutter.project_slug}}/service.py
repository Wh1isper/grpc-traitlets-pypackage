from pb.helloworld_pb2 import (
    HelloRequest,
    HelloReply,
)
from pb import helloworld_pb2_grpc
from {{cookiecutter.project_slug}}.plogger import get_logger


class Service(helloworld_pb2_grpc.GreeterServicer):
    plogger = get_logger("Service")

    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def add_to_server(parent, server):
        """注册该服务到server中
        :param parent: application实例
        :param server: server实例
        :return:
        """
        Service.plogger.info('add Service to server')
        helloworld_pb2_grpc.add_GreeterServicer_to_server(Service(parent), server)

    def SayHello(self, request, context):
        return HelloReply(message='Hello, %s!' % request.name)
