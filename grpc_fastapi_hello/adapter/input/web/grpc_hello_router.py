from fastapi import APIRouter, Request
import hello_pb2 as pb

grpc_hello_router = APIRouter()

@grpc_hello_router.get("/say-hello")
async def say_hello(
    request: Request,
    name: str = "World",
):
    stub = request.app.state.grpc_stub
    response = await stub.SayHello(
        pb.HelloRequest(name=name)
    )
    return {"message": response.message}
