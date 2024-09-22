import grpc
from google.protobuf import json_format
import reporting_pb2
import reporting_pb2_grpc
import json
from validation import Spaceship as ValidatedSpaceship

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reporting_pb2_grpc.ReportingStub(channel)
        response_stream = stub.GetSpaceship(reporting_pb2.Coordinates(x=1, y=2, z=3, x2=4, y2=5, z2=6))
        ship_count: int = 0
        validate_count: int = 0
        for spaceship in response_stream:
            spaceship_dict = json_format.MessageToDict(
                spaceship,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True
            )
            # print(spaceship_dict)
            ship_count += 1
            try:
                spaceship_validate = ValidatedSpaceship(**spaceship_dict)
                json_output = json.dumps(spaceship_validate.dict(), indent=2)
                print(json_output)
                validate_count += 1
            except:
                pass
                # print("Wrong spaceship received")
        print(f"Spaceship count: {ship_count}, validate count: {validate_count}")


if __name__ == '__main__':
    run()
