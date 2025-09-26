from fastapi import APIRouter

from download_agent.download import download_document
from multi_agent_document.parser_agent.parse import parse_document_agent

from summarize_agent.summarize import summarize_agent
from answer_agent.answer import answer_agent

multiAgentDocumentRouter = APIRouter()

@multiAgentDocumentRouter.post("/single-doc-agent/request-process")
async def multi_agent_process(doc_url: str, question: str):
    content = await download_document(doc_url)
    text = await parse_document_agent(content, doc_url)
    summary = await summarize_agent(text)
    answer = await answer_agent(summary, question)
    return {"summary": summary, "answer": answer}
