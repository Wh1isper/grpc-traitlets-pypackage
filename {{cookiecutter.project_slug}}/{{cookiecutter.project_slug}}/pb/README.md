# protos for project

``` shell
python -m grpc_tools.protoc -I./{{cookiecutter.project_slug}}/pb --python_out=./{{cookiecutter.project_slug}}/pb --grpc_python_out=./{{cookiecutter.project_slug}}/pb ./{{cookiecutter.project_slug}}/pb/helloworld.proto
```
