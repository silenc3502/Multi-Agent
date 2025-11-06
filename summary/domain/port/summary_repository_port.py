from abc import ABC, abstractmethod
from typing import List

from summary.domain.entity.summary import Summary


class SummaryRepositoryPort(ABC):
    @abstractmethod
    def save(self, summary: Summary) -> Summary: ...

    @abstractmethod
    def find_by_document_id(self, document_id: int) -> List[Summary]: ...
