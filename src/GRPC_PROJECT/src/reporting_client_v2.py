import grpc
from google.protobuf import json_format
import reporting_pb2
import reporting_pb2_grpc
import json
from validation import Spaceship as ValidatedSpaceship
import argparse


def run(x: float, y: float, z: float, t: float, e: float, o: float):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reporting_pb2_grpc.ReportingStub(channel)
        response_stream = stub.GetSpaceship(reporting_pb2.Coordinates(x=x, y=y, z=z, x2=t, y2=e, z2=o))

        ship_count: int = 0
        validate_count: int = 0
        for spaceship in response_stream:
            spaceship_dict = json_format.MessageToDict(
                                spaceship,
                                preserving_proto_field_name=True,
                                always_print_fields_with_no_presence=True
                            )
            ship_count += 1
            try:
                            spaceship_validate = ValidatedSpaceship(**spaceship_dict)
                            json_output = json.dumps(spaceship_validate.dict(), indent=2)
                            print(json_output)
                            validate_count += 1
            except:
                            pass

        print(f"Spaceship count: {ship_count}, validated: {validate_count}")



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("ra_hours", type=float, help="Часы прямого восхождения (RA)", default=0)
    parser.add_argument("ra_minutes", type=float, help="Минуты прямого восхождения (RA)", default=0)
    parser.add_argument("ra_seconds", type=float, help="Секунды прямого восхождения (RA)", default=0)
    parser.add_argument("dec_degrees", type=float, help="Градусы склонения (DEC)", default=0)
    parser.add_argument("dec_minutes", type=float, help="Минуты склонения (DEC)", default=0)
    parser.add_argument("dec_seconds", type=float, help="Секунды склонения (DEC)", default=0)
    # Парсинг аргументов
    args = parser.parse_args()
    run(args.ra_hours, args.ra_minutes, args.ra_seconds, args.dec_degrees, args.dec_minutes, args.dec_seconds)

if __name__ == '__main__':
    main()


