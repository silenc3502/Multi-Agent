from summary.domain.entity.summary import Summary
from summary.domain.port.summary_repository_port import SummaryRepositoryPort


class GenerateSummaryUseCase:
    def __init__(self, summary_repo: SummaryRepositoryPort, summary_agent: SummaryAgent):
        self.summary_repo = summary_repo
        self.summary_agent = summary_agent

    def execute(self, document_id: int, content: str) -> Summary:
        # LangGraph 기반 Multi-Agent 호출
        summaries = self.summary_agent.generate(content)

        summary = Summary(
            document_id=document_id,
            bullet=summaries["bullet"],
            abstract=summaries["abstract"],
            casual=summaries["casual"],
            final_summary=summaries["final_summary"],
        )
        return self.summary_repo.save(summary)
