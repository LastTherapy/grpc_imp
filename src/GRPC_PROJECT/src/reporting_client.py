import grpc
from google.protobuf import json_format
import reporting_pb2
import reporting_pb2_grpc
import argparse

def run(x: float, y: float, z: float, t: float, e: float, o: float):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reporting_pb2_grpc.ReportingStub(channel)
        response_stream = stub.GetSpaceship(reporting_pb2.Coordinates(x=x, y=y, z=z, x2=t, y2=e, z2=o))

        for spaceship in response_stream:
            print(json_format.MessageToJson(spaceship, preserving_proto_field_name=True,
                                            always_print_fields_with_no_presence=True))



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
