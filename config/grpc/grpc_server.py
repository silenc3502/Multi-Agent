import threading
from concurrent import futures
import grpc
import hello_pb2 as pb
import hello_pb2_grpc as pb_grpc

class HelloService(pb_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        return pb.HelloResponse(message=f"Hello, {request.name}!")

def start_grpc_server(stop_event: threading.Event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    pb_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")

    stop_event.wait()   # 스레드용 Event
    server.stop(0)
    print("gRPC server stopped")
