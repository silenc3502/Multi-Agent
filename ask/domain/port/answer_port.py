from abc import ABC, abstractmethod

from ask.domain.answer import Answer


class AnswerPort(ABC):

    @abstractmethod
    def save(self, answer: Answer) -> Answer:
        pass
