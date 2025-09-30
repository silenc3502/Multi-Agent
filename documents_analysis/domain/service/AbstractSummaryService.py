import asyncio

from multi_agent_document.loader.model_loader import summarize_pipeline


class AbstractSummaryService:
    async def summarize(self, text: str) -> str:
        prompt = f"Write a scholarly abstract (3-5 sentences) for the following text:\n\n{text}"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: summarize_pipeline(prompt, max_length=300, min_length=80, do_sample=False)
        )
        return result[0].get("summary_text", "")