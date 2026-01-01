# fastapi_config.py
import threading
from fastapi import FastAPI
import grpc
import hello_pb2_grpc as pb_grpc
from config.grpc.grpc_server import start_grpc_server

async def init_fastapi_lifespan(app: FastAPI):
    try:
        stop_event = threading.Event()
        app.state.stop_event = stop_event

        server_thread = threading.Thread(target=start_grpc_server, args=(stop_event,), daemon=True)
        server_thread.start()

        app.state.grpc_channel = grpc.aio.insecure_channel("localhost:50051")
        app.state.grpc_stub = pb_grpc.HelloServiceStub(app.state.grpc_channel)

        yield
    finally:
        await app.state.grpc_channel.close()
        stop_event.set()
        server_thread.join()
