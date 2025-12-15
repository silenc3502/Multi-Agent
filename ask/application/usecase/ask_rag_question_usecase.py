from datetime import datetime
from typing import List

from ask.domain.answer import Answer
from ask.domain.port.answer_port import AnswerPort
from ask.domain.port.question_port import QuestionPort
from ask.domain.question import Question
from ask.infrastructure.client.rag_agent import RAGAgent


class AskRAGQuestionUseCase:
    def __init__(self, question_port: QuestionPort, answer_port: AnswerPort, agent: RAGAgent):
        self.question_port = question_port
        self.answer_port = answer_port
        self.agent = agent

    def execute(self, question_text: str, asker_id: int):
        # 1. 질문 저장
        question = Question(
            id=None,
            content=question_text,
            created_at=datetime.utcnow(),
            asker_id=asker_id
        )
        saved_question = self.question_port.save(question)

        # 2. RAG 조회
        context_texts = self.agent.query_documents(question_text)

        # 3. 답변 생성
        answer_text = self.agent.generate_answer(question_text, context_texts)

        # 4. 답변 저장
        answer = Answer(
            id=None,
            question_id=saved_question.id,
            responder_id=asker_id,
            content=answer_text,
            created_at=datetime.utcnow()
        )
        saved_answer = self.answer_port.save(answer)

        return saved_answer
