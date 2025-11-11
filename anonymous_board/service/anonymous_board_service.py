from abc import ABC, abstractmethod
from anonymous_board.entity.anonymous_board import AnonymousBoard
from typing import List, Optional

class AnonymousBoardService(ABC):

    @abstractmethod
    def create_board(self, title: str, content: str) -> AnonymousBoard:
        pass

    @abstractmethod
    def list_boards(self) -> List[AnonymousBoard]:
        pass

    @abstractmethod
    def get_board(self, board_id: str) -> Optional[AnonymousBoard]:
        pass
