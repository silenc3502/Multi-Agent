from typing import List
from domain.board import Board
from application.port.board_repository_port import BoardRepositoryPort

class BoardUsecase:
    def __init__(self, repository: BoardRepositoryPort):
        self.repository = repository

    def create_board(self, title: str, content: str, author_id: str) -> Board:
        board = Board.create(title, content, author_id)
        return self.repository.save(board)

    def get_board(self, board_id: int) -> Board:
        board = self.repository.find_by_id(board_id)
        if not board:
            raise ValueError("Board not found")
        return board

    def get_boards_by_author(self, author_id: str) -> List[Board]:
        return self.repository.find_by_author(author_id)

    def delete_board(self, board_id: int):
        self.repository.delete(board_id)
