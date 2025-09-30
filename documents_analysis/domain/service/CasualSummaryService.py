import asyncio

from multi_agent_document.loader.model_loader import summarize_pipeline


class CasualSummaryService:
    async def summarize(self, text: str) -> str:
        prompt = f"Explain the following text in a simple, casual way for a non-expert:\n\n{text}"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: summarize_pipeline(prompt, max_length=250, min_length=50, do_sample=False)
        )
        return result[0].get("summary_text", "")