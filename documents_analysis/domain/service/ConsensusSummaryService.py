import asyncio

from multi_agent_document.loader.model_loader import summarize_pipeline


class ConsensusSummaryService:
    async def summarize(self, summaries: list[str]) -> str:
        joined = "\n\n".join(f"- {s}" for s in summaries if s)
        prompt = f"""Here are multiple summaries from different perspectives:
{joined}

Create a final comprehensive summary that integrates all perspectives."""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: summarize_pipeline(prompt, max_length=300, min_length=80, do_sample=False)
        )
        return result[0].get("summary_text", "")