import grpc
from google.protobuf import json_format
import reporting_pb2
import reporting_pb2_grpc
import json

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reporting_pb2_grpc.ReportingStub(channel)
        response_stream = stub.GetSpaceship(reporting_pb2.Coordinates(x=1, y=2, z=3, x2=4, y2=5, z2=6))
        for spaceship in response_stream:
            print(json_format.MessageToJson(spaceship, preserving_proto_field_name=True,
                                            always_print_fields_with_no_presence=True))


if __name__ == '__main__':
    run()
