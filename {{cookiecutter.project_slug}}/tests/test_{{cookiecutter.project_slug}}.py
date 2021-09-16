# import for support grpc
from utilities import grpc_add_to_server, grpc_servicer, grpc_stub_cls, JobThread
from {{cookiecutter.project_slug}}.pb.helloworld_pb2 import (
    HelloRequest,
    HelloReply,
)
import pytest


def test_helloworld(grpc_stub):
    request_str = 'you'
    response = grpc_stub.SayHello(HelloRequest(name=request_str))
    assert response.message == f'Hello, {request_str}!'

if __name__ == '__main__':
    pytest.main()
