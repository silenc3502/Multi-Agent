from abc import ABC, abstractmethod
from typing import List

from summary.domain.entity.answer import Answer


class AnswerRepositoryPort(ABC):
    @abstractmethod
    def save(self, answer: Answer) -> Answer: ...

    @abstractmethod
    def find_by_document_id(self, document_id: int) -> List[Answer]: ...
