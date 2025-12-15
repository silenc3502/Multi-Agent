from typing import List

from ask.infrastructure.client.rag_agent import RAGAgent

class AddDocumentsUseCase:
    def __init__(self, agent: RAGAgent):
        self.agent = agent

    def execute(self, documents: List[str]) -> int:
        """
        문서를 RAG Agent에 추가하고, 추가된 문서 개수를 반환
        """
        if not documents:
            return 0

        self.agent.add_documents(documents)
        return len(documents)
