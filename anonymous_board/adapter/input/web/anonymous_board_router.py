from fastapi import APIRouter, HTTPException

from anonymous_board.application.usecase.anonymous_board_usecase import AnonymousBoardUseCase
from anonymous_board.infrastructure.repository.anonymous_board_repository_impl import AnonymousBoardRepositoryImpl

anonymous_board_router = APIRouter()
usecase = AnonymousBoardUseCase(AnonymousBoardRepositoryImpl())

@anonymous_board_router.post("/create")
def create_board(title: str, content: str, author: str = None):
    return usecase.create_board(title, content, author)

@anonymous_board_router.get("/list")
def list_boards():
    return usecase.list_boards()

@anonymous_board_router.get("/read/{board_id}")
def get_board(board_id: int):
    board = usecase.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@anonymous_board_router.delete("/delete/{board_id}")
def delete_board(board_id: int):
    usecase.delete_board(board_id)
    return {"message": "Deleted successfully"}
