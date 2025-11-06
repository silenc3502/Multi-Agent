import asyncio

from multi_agent_document.loader.model_loader import summarize_pipeline


class AnswerService:
    async def answer(self, final_summary: str, question: str) -> str:
        prompt = f"Based on the following summary:\n{final_summary}\n\nAnswer the question:\n{question}"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: summarize_pipeline(prompt, max_length=250, min_length=50, do_sample=False)
        )
        return result[0].get("summary_text", "")
