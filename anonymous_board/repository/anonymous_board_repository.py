from abc import ABC, abstractmethod
from anonymous_board.entity.anonymous_board import AnonymousBoard
from typing import List, Optional

class AnonymousBoardRepository(ABC):

    @abstractmethod
    def create(self, title: str, content: str) -> AnonymousBoard:
        pass

    @abstractmethod
    def list_all(self) -> List[AnonymousBoard]:
        pass

    @abstractmethod
    def get(self, board_id: str) -> Optional[AnonymousBoard]:
        pass
