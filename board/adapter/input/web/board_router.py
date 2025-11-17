# from fastapi import APIRouter, Depends, Request, Response, Cookie
# from fastapi.responses import JSONResponse
#
# from board.application.usecase.board_usecase import BoardUsecase
# from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl
# from social_oauth.adapter.input.web.google_oauth2_router import redis_client
#
# board_router = APIRouter(prefix="/board", tags=["board"])
# board_repository_impl = BoardRepositoryImpl()
# board_usecase = BoardUsecase(board_repository_impl)
#
# # 세션으로 사용자 확인
# def get_current_user(session_id: str = Cookie(None)) -> str:
#     if not session_id:
#         raise ValueError("No session_id")
#     access_token = redis_client.get(session_id)
#     if not access_token:
#         raise ValueError("Invalid session")
#     # access_token으로 user_id 조회
#     user_id = some_user_service.get_user_id(access_token)
#     return user_id
#
# @board_router.post("/")
# async def create_board(request: Request, title: str, content: str, user_id: str = Depends(get_current_user)):
#     board = board_usecase.create_board(title, content, user_id)
#     return JSONResponse({"id": board.id, "title": board.title})
#
# @board_router.get("/{board_id}")
# async def get_board(board_id: int):
#     board = board_usecase.get_board(board_id)
#     return JSONResponse({"id": board.id, "title": board.title, "content": board.content, "author_id": board.author_id})
#
# @board_router.get("/me")
# async def get_my_boards(user_id: str = Depends(get_current_user)):
#     boards = board_usecase.get_boards_by_author(user_id)
#     return JSONResponse([{"id": b.id, "title": b.title, "content": b.content} for b in boards])
#
# @board_router.delete("/{board_id}")
# async def delete_board(board_id: int, user_id: str = Depends(get_current_user)):
#     board = board_usecase.get_board(board_id)
#     if board.author_id != user_id:
#         return JSONResponse({"error": "Not allowed"}, status_code=403)
#     board_usecase.delete_board(board_id)
#     return JSONResponse({"result": "deleted"})
