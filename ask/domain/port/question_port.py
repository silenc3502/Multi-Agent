from abc import ABC, abstractmethod

from ask.domain.question import Question


class QuestionPort(ABC):

    @abstractmethod
    def save(self, question: Question) -> Question:
        pass
