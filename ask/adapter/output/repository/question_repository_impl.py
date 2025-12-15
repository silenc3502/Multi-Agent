from sqlalchemy.orm import Session

from ask.domain.question import Question
from ask.domain.port.question_port import QuestionPort
from ask.infrastructure.orm.question_orm import QuestionOrm
from config.database.session import SessionLocal


class QuestionRepositoryImpl(QuestionPort):

    def save(self, question: Question) -> Question:
        db: Session = SessionLocal()
        try:
            orm = QuestionOrm(
                asker_id=question.asker_id,
                content=question.content,
                created_at=question.created_at
            )

            db.add(orm)
            db.commit()
            db.refresh(orm)

            question.id = orm.id
            question.created_at = orm.created_at

            return question

        except:
            db.rollback()
            raise
        finally:
            db.close()
