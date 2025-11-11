from fastapi import APIRouter, HTTPException
from typing import List

from anonymous_board.controller.request.create_anonymous_board_request import CreateAnonymousBoardRequest
from anonymous_board.controller.response.anonymous_board_response import AnonymousBoardResponse
from anonymous_board.service.anonymous_board_service_impl import AnonymousBoardServiceImpl

anonymous_board_controller = APIRouter(prefix="/board", tags=["boards"])
board_service = AnonymousBoardServiceImpl.getInstance()


@anonymous_board_controller.post("/create", response_model=AnonymousBoardResponse)
def create_board(request: CreateAnonymousBoardRequest):
    board = board_service.create_board(request.title, request.content)
    return AnonymousBoardResponse(
        id=board.id,
        title=board.title,
        content=board.content,
        created_at=board.created_at.isoformat()
    )

@anonymous_board_controller.get("/list", response_model=List[AnonymousBoardResponse])
def list_boards():
    boards = board_service.list_boards()
    return [
        AnonymousBoardResponse(
            id=b.id,
            title=b.title,
            content=b.content,
            created_at=b.created_at.isoformat()
        ) for b in boards
    ]

@anonymous_board_controller.get("/{board_id}", response_model=AnonymousBoardResponse)
def get_board(board_id: str):
    try:
        board = board_service.get_board(board_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")
    return AnonymousBoardResponse(
        id=board.id,
        title=board.title,
        content=board.content,
        created_at=board.created_at.isoformat()
    )
