from app.model_loader import tokenizer, model

async def answer_agent(summary: str, question: str) -> str:
    prompt = f"Document summary:\n{summary}\n\nQuestion: {question}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
