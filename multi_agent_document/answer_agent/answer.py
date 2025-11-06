from multi_agent_document.loader.model_loader import qa_pipeline

async def answer_agent(summary: str, question: str) -> str:
    prompt = f"Document summary:\n{summary}\n\nQuestion: {question}\nAnswer:"
    result = qa_pipeline(prompt, max_length=200, do_sample=False)
    return result[0]["generated_text"]
