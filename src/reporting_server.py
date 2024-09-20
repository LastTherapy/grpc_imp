import random
import grpc
import reporting_pb2_grpc
import reporting_pb2
from concurrent import futures

spaceship_names = ["Normandy", "Executor", "Falcon"]
first_names = ["John", "Jane", "Michael", "Sarah", "Alex", "Emily", "David", "Sophia", "James", "Olivia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Taylor", "Anderson", "Thomas", "Moore", "Jackson", "White"]
ranks = ["Captain", "Commander", "Lieutenant", "Ensign", "Major", "Colonel", "Admiral", "Commodore", "Sergeant", "Corporal"]

class ReportingServicer(reporting_pb2_grpc.ReportingServicer):


    def GetSpaceship(self, request, context):
        alignment = random.choice(list(reporting_pb2.Alignment.DESCRIPTOR.values_by_name.keys()))
        space_class = random.choice(list(reporting_pb2.SpaceClass.DESCRIPTOR.values_by_name.keys()))
        space_length = random.random()*20000
        crew_size = random.randint(1, 10)
        armed = random.choice([True, False])


        ship = reporting_pb2.Spaceship(
            alignment= alignment,
            name= random.choice(spaceship_names),
            length= space_length,
            crew_size= crew_size,
            armed=armed,
            officers= [reporting_pb2.Officer(
                first_name = random.choice(first_names),
                last_name = random.choice(last_names),
                rank = random.choice(ranks)
                ) for _ in range(crew_size)]
            )

        # because class is a keyword
        setattr(ship, 'class', space_class)
        yield ship

# Запуск gRPC сервера
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reporting_pb2_grpc.add_ReportingServicer_to_server(ReportingServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()