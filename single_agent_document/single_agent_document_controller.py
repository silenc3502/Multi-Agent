from fastapi import APIRouter, Request
import aiohttp

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from utility.document_parser import parse_document

singleAgentDocumentRouter = APIRouter()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)


async def load_document(doc_url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(doc_url) as resp:
            content = await resp.read()
    return parse_document(content, doc_url)


async def summarize_text(text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="다음 문서의 중요한 내용을 요약해 주세요:\n{text}"
    )
    return llm(prompt.format(text=text))


async def answer_question(summaries: str, question: str) -> str:
    prompt = f"다음 내용을 기반으로 질문에 답해주세요:\n{summaries}\n질문: {question}"
    return llm(prompt)


@singleAgentDocumentRouter.post("/async-lab/request-process")
async def request_async_process(doc_url: str, question: str):
    text = await load_document(doc_url)
    summary = await summarize_text(text)
    answer = await answer_question(summary, question)
    return {"summary": summary, "answer": answer}
