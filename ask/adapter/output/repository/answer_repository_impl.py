from sqlalchemy.orm import Session

from ask.domain.answer import Answer
from ask.domain.port.answer_port import AnswerPort
from ask.infrastructure.orm.answer_orm import AnswerOrm
from config.database.session import SessionLocal


class AnswerRepositoryImpl(AnswerPort):

    def save(self, answer: Answer) -> Answer:
        db: Session = SessionLocal()
        try:
            orm = AnswerOrm(
                question_id=answer.question_id,
                responder_id=answer.responder_id,
                content=answer.content,
                created_at=answer.created_at
            )

            db.add(orm)
            db.commit()
            db.refresh(orm)

            # Domain 객체에 반영
            answer.id = orm.id
            answer.created_at = orm.created_at

            return answer

        except:
            db.rollback()
            raise
        finally:
            db.close()
