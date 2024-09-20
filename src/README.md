pip install grpcio grpcio-tools protobuf

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. reporting.proto

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. reporting.proto
