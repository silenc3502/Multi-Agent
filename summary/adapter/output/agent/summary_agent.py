from langgraph import Graph
from langchain import LLMChain


class SummaryAgent:
    def __init__(self, llm_model):
        self.graph = Graph()
        self.llm = llm_model

    def generate(self, text: str) -> dict:
        # 실제로는 그래프 기반 멀티 노드 (bullet, abstract, casual, final_summary)
        bullet = self.llm(f"Summarize in bullet points: {text}")
        abstract = self.llm(f"Summarize in academic abstract form: {text}")
        casual = self.llm(f"Summarize casually: {text}")
        final_summary = self.llm(f"Integrate all summaries briefly: {text}")

        return {
            "bullet": bullet,
            "abstract": abstract,
            "casual": casual,
            "final_summary": final_summary,
        }
