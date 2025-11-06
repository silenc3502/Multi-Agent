from multi_agent_document.loader.model_loader import summarize_pipeline

async def bullet_summarizer(text: str) -> str:
    prompt = f"Summarize the following text into 5 concise bullet points:\n\n{text}"
    result = summarize_pipeline(prompt, max_length=250, min_length=50, do_sample=False)
    return result[0].get("summary_text", "")

async def abstract_summarizer(text: str) -> str:
    prompt = f"Write a scholarly abstract (3-5 sentences) for the following text:\n\n{text}"
    result = summarize_pipeline(prompt, max_length=300, min_length=80, do_sample=False)
    return result[0].get("summary_text", "")

async def casual_summarizer(text: str) -> str:
    prompt = f"Explain the following text in a simple, casual way for a non-expert:\n\n{text}"
    result = summarize_pipeline(prompt, max_length=250, min_length=50, do_sample=False)
    return result[0].get("summary_text", "")

async def consensus_summarizer(summaries: list[str]) -> str:
    joined = "\n\n".join(f"- {s}" for s in summaries if s)
    prompt = f"""Here are multiple summaries from different perspectives:
{joined}

Create a final comprehensive summary that integrates all perspectives."""
    result = summarize_pipeline(prompt, max_length=300, min_length=80, do_sample=False)
    return result[0].get("summary_text", "")
