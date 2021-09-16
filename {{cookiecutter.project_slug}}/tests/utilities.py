import sys
import os
import threading
from glob import glob

dir_prefix = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.abspath(os.path.join(dir_prefix, '../{{cookiecutter.project_slug}}'))
dir_path = glob(project_dir + '/**/', recursive=True)
project_path = []
while dir_path:
    top = os.path.join(project_dir, dir_path.pop(0))
    if not top.endswith('__pycache__/'):
        project_path.append(top)

for p in project_path:
    print(f"adding {p} dir to tests path")
sys.path.extend(project_path)

import pytest
from {{cookiecutter.project_slug}}.app import ExampleApplication


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from {{cookiecutter.project_slug}}.pb.helloworld_pb2_grpc import add_GreeterServicer_to_server

    return add_GreeterServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    from {{cookiecutter.project_slug}}.service import Service
    ExampleApplication().initialize()

    return Service(ExampleApplication())


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from {{cookiecutter.project_slug}}.pb.helloworld_pb2_grpc import GreeterStub

    return GreeterStub


class JobThread(threading.Thread):
    def __init__(self, target, args=None, kwargs=None):
        super(JobThread, self).__init__()
        self.target = target
        if not args:
            args = []
        self.args = args
        if not kwargs:
            kwargs = dict()
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.target(*self.args, **self.kwargs)

    def get_result(self):
        return self.result
