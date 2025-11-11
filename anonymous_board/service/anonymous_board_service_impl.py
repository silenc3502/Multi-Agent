from anonymous_board.repository.anonymous_board_repository_impl import AnonymousBoardRepositoryImpl
from anonymous_board.service.anonymous_board_service import AnonymousBoardService


class AnonymousBoardServiceImpl(AnonymousBoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repo = AnonymousBoardRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create_board(self, title: str, content: str):
        return self.repo.create(title, content)

    def list_boards(self):
        return self.repo.list_all()

    def get_board(self, board_id: str):
        board = self.repo.get(board_id)
        if not board:
            raise ValueError("Board not found")
        return board
