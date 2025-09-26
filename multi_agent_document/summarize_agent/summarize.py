from app.model_loader import llm_pipeline

async def summarize_agent(text: str) -> str:
    result = llm_pipeline(text, max_length=300, min_length=50, do_sample=False)
    return result[0].get("summary_text", "")
