import argparse

import grpc
from google.protobuf import json_format
import reporting_pb2
import reporting_pb2_grpc
import json
from validation import Spaceship
from storage import save_ship, find_traitors


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
            # print(spaceship_dict)
            ship_count += 1

            try:
                spaceship_validate = Spaceship(**spaceship_dict)
                json_output = json.dumps(spaceship_validate.dict(), indent=2)
                # print(json_output)
                validate_count += 1
                save_ship(spaceship_dict)
            except:
                pass
                # print("Wrong spaceship received")

        print(f"Spaceship count: {ship_count}, validated count: {validate_count}")


def main():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="commands", help="Subparser help")
        scan_command = subparsers.add_parser("scan", help="Scan help")
        subparsers.add_parser("list-traitors", help="List traitors help")

        scan_command.add_argument("ra_hours", type=float, help="Часы прямого восхождения (RA)", default=0)
        scan_command.add_argument("ra_minutes", type=float, help="Минуты прямого восхождения (RA)", default=0)
        scan_command.add_argument("ra_seconds", type=float, help="Секунды прямого восхождения (RA)", default=0)
        scan_command.add_argument("dec_degrees", type=float, help="Градусы склонения (DEC)", default=0)
        scan_command.add_argument("dec_minutes", type=float, help="Минуты склонения (DEC)", default=0)
        scan_command.add_argument("dec_seconds", type=float, help="Секунды склонения (DEC)", default=0)
        # Парсинг аргументов
        args = parser.parse_args()
        if args.commands == "scan":
            run(args.ra_hours, args.ra_minutes, args.ra_seconds, args.dec_degrees, args.dec_minutes, args.dec_seconds)
        elif args.commands == "list-traitors":
            find_traitors()


if __name__ == '__main__':
    main()
