from sqlalchemy.orm import Session

from summary.adapter.output.persistence.summary_orm import SummaryORM
from summary.domain.entity.summary import Summary
from summary.domain.port.summary_repository_port import SummaryRepositoryPort


class SummaryRepositoryAdapter(SummaryRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def save(self, summary: Summary) -> Summary:
        orm = SummaryORM(**summary.dict(exclude_unset=True))
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return Summary(**orm.__dict__)

    def find_by_document_id(self, document_id: int):
        results = self.session.query(SummaryORM).filter(SummaryORM.document_id == document_id).all()
        return [Summary(**r.__dict__) for r in results]
