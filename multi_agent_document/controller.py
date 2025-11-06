import asyncio
from fastapi import APIRouter
from multi_agent_document.request import MultiAgentRequest

from multi_agent_document.download_agent.download import download_document
from utility.document_parser import parse_document  # parse 함수 직접 사용

from multi_agent_document.summarize_agent.summarize import (
    bullet_summarizer,
    abstract_summarizer,
    casual_summarizer,
    consensus_summarizer
)
from multi_agent_document.answer_agent.answer import answer_agent

multiAgentDocumentRouter = APIRouter()

async def load_and_parse_document(doc_url: str) -> str:
    from multi_agent_document.download_agent.download import download_document, get_cache_filename

    print(f"[DEBUG] 다운로드 시작: {doc_url}")
    content = await download_document(doc_url)

    cache_path = get_cache_filename(doc_url)
    print(f"[DEBUG] 캐시된 파일 경로: {cache_path}")

    # 디버그: 다운로드된 PDF 저장
    debug_path = "debug_downloaded.pdf"
    with open(debug_path, "wb") as f:
        f.write(content)
    print(f"[DEBUG] 다운로드된 PDF 저장: {debug_path} ({len(content)} bytes)")

    # 바이트(content) 전달
    print("[DEBUG] 파싱 시작")
    text = parse_document(content, cache_path)
    print(f"[DEBUG] 파싱 완료, 길이: {len(text)} characters")

    # 파싱된 텍스트 저장
    debug_text_path = "debug_parsed_text_multiagent.txt"
    with open(debug_text_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[DEBUG] 파싱된 텍스트 저장: {debug_text_path}")

    return text


@multiAgentDocumentRouter.post("/multi-doc-agent/request-process")
async def multi_agent_process(request: MultiAgentRequest):
    text = await load_and_parse_document(request.doc_url)

    if not text:
        return {"error": "문서 파싱 실패", "details": "파싱된 텍스트가 없습니다."}

    bullet, abstract, casual = await asyncio.gather(
        bullet_summarizer(text),
        abstract_summarizer(text),
        casual_summarizer(text)
    )

    final_summary = await consensus_summarizer([bullet, abstract, casual])
    answer = await answer_agent(final_summary, request.question)

    return {
        "summaries": {
            "bullet": bullet,
            "abstract": abstract,
            "casual": casual,
        },
        "final_summary": final_summary,
        "answer": answer
    }

