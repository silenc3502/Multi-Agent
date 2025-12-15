from datetime import datetime
from ask.domain.answer import Answer
from ask.domain.port.answer_port import AnswerPort
from ask.domain.port.question_port import QuestionPort
from ask.domain.question import Question


class AskQuestionUseCase:

    def __init__(self, question_port, answer_port, agent):
        self.question_port = question_port
        self.answer_port = answer_port
        self.agent = agent

    def execute(self, question_text: str, asker_id: int):  # ← user_id 추가
        # 1. 질문 저장
        question = Question(
            id=None,
            content=question_text,
            created_at=datetime.utcnow(),
            asker_id=asker_id  # ← 필수
        )
        saved_question = self.question_port.save(question)

        # 2. 에이전트로 응답 생성
        answer_text = self.agent.ask(question_text)

        # 3. 응답 저장
        answer = Answer(
            id=None,
            question_id=saved_question.id,
            responder_id=asker_id,
            content=answer_text,
            created_at=datetime.utcnow()
        )
        saved_answer = self.answer_port.save(answer)

        return saved_answer
