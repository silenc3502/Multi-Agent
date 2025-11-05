from langgraph.graph import StateGraph
from transformers import pipeline
import asyncio

# 1️⃣ StateSchema 직접 정의
class MyStateSchema:
    def __init__(self):
        self.bullet_summary_done = False
        self.abstract_summary_done = False
        self.casual_summary_done = False
        self.final_summary_done = False
        self.answer_generated = False

    def __hash__(self):
        # StateGraph 내부에서 hash 필요하므로 정의
        return hash((
            self.bullet_summary_done,
            self.abstract_summary_done,
            self.casual_summary_done,
            self.final_summary_done,
            self.answer_generated
        ))

    def __eq__(self, other):
        if not isinstance(other, MyStateSchema):
            return False
        return (
            self.bullet_summary_done == other.bullet_summary_done and
            self.abstract_summary_done == other.abstract_summary_done and
            self.casual_summary_done == other.casual_summary_done and
            self.final_summary_done == other.final_summary_done and
            self.answer_generated == other.answer_generated
        )


class MultiAgentAnalyzer:
    def __init__(self):
        self.generator = pipeline(
            "text-generation",
            model="gpt2",
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7
        )

    async def generate_text(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: self.generator(prompt)[0]["generated_text"])
        return result.strip()

    async def run(self, local_path: str):
        state_schema = MyStateSchema()
        graph = StateGraph(state_schema)

        bullet_summary = await self.generate_text(f"Summarize key points from {local_path}. Use bullet points.")
        state_schema.bullet_summary_done = True

        abstract_summary = await self.generate_text(f"Create an academic abstract based on {local_path}.")
        state_schema.abstract_summary_done = True

        casual_summary = await self.generate_text(f"Make a casual summary for {local_path}.")
        state_schema.casual_summary_done = True

        final_summary = await self.generate_text("Merge all previous summaries into one comprehensive overview.")
        state_schema.final_summary_done = True

        answer = await self.generate_text(f"Answer potential user questions based on {local_path}.")
        state_schema.answer_generated = True

        # 🔹 StateGraph는 반환하지 않고 dict로 변환
        state_dict = {
            "bullet_summary_done": state_schema.bullet_summary_done,
            "abstract_summary_done": state_schema.abstract_summary_done,
            "casual_summary_done": state_schema.casual_summary_done,
            "final_summary_done": state_schema.final_summary_done,
            "answer_generated": state_schema.answer_generated,
        }

        return {
            "summaries": {
                "bullet": bullet_summary,
                "abstract": abstract_summary,
                "casual": casual_summary,
            },
            "final_summary": final_summary,
            "answer": answer,
            "state": state_dict
        }
