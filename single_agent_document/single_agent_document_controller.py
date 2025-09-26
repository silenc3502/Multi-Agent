# single_agent_document/single_agent_document_controller.py
import hashlib
import logging
import os
import re
from fastapi import APIRouter
import aiohttp

from app.model_loader import llm_pipeline, model, tokenizer
from single_agent_document.request_data import RequestData
from utility.document_parser import parse_document

logger = logging.getLogger("single_agent_document")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

DOWNLOAD_CACHE_DIR = "downloaded_docs"
os.makedirs(DOWNLOAD_CACHE_DIR, exist_ok=True)

singleAgentDocumentRouter = APIRouter()

def get_cache_filename(url: str) -> str:
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return os.path.join(DOWNLOAD_CACHE_DIR, f"{url_hash}.pdf")

async def load_document(doc_url: str) -> str:
    logger.info("Loading document: %s", doc_url)

    cache_path = get_cache_filename(doc_url)
    text = ""

    if os.path.exists(cache_path):
        logger.info("Cache hit: %s", cache_path)
        with open(cache_path, "rb") as f:
            content = f.read()
        text = parse_document(content, cache_path)
    else:
        logger.info("Cache miss, downloading document")
        async with aiohttp.ClientSession() as session:
            async with session.get(doc_url) as resp:
                logger.info("Response status: %d", resp.status)
                if resp.status != 200:
                    raise Exception(f"Failed to download {doc_url}")
                content = await resp.read()
                logger.info("Downloaded %d bytes", len(content))
                with open(cache_path, "wb") as f:
                    f.write(content)
                    logger.info("Saved to cache: %s", cache_path)
                text = parse_document(content, cache_path)

    logger.info("Extracted text length: %d chars", len(text or ""))
    return text

def text_stats(text: str) -> dict:
    if not text:
        return {"length": 0, "snippet": "", "lorem_count": 0, "words": 0}
    snippet = text[:2000]
    lorem_count = len(re.findall(r"lorem ipsum", text, flags=re.I))
    words = len(re.findall(r"\w+", text))
    latin_words = sum(
        1
        for w in re.findall(r"\b[a-zA-Z]+\b", text.lower())
        if w
        in {
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "nunc",
            "maecenas",
            "ulllamcorper",
            "praesent",
            "vestibulum",
            "curabitur",
        }
    )
    return {
        "length": len(text),
        "snippet": snippet,
        "lorem_count": lorem_count,
        "words": words,
        "latin_keyword_count": latin_words,
    }

def chunk_text(text: str, chunk_size: int = 300) -> list[str]:
    """토큰 제한을 피하기 위해 텍스트를 분할"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks

async def summarize_text(text: str) -> str:
    logger.info("SUMMARIZE - called, input length=%d", len(text or ""))
    chunks = chunk_text(text, chunk_size=300)  # 토큰 제한을 위해 분할
    summaries = []

    for i, chunk in enumerate(chunks):
        logger.info(f"Summarizing chunk {i+1}/{len(chunks)} length={len(chunk)}")
        try:
            result = llm_pipeline(chunk, max_length=200, min_length=50, do_sample=False)
            summaries.append(result[0]["summary_text"])
        except Exception as e:
            logger.exception(f"Chunk {i+1} summarization failed: {e}")

    final_summary = " ".join(summaries)
    logger.info("SUMMARIZE - final summary length=%d", len(final_summary))
    return final_summary

async def answer_question(summaries: str, question: str) -> str:
    logger.info("ANSWER - called, summary_len=%d, question_len=%d", len(summaries or ""), len(question or ""))
    logger.info("ANSWER - summary preview: %s", (summaries or "")[:300].replace("\n", "\\n"))
    prompt = f"Document summary:\n{summaries}\n\nQuestion: {question}\nAnswer:"
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = model.generate(**inputs, max_length=200)
        gen = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("ANSWER - generated answer preview: %s", gen[:300].replace("\n", "\\n"))
        return gen
    except Exception as e:
        logger.exception("ANSWER - generation failed: %s", e)
        return "질문에 답변할 수 없습니다. (모델 오류)"

@singleAgentDocumentRouter.post("/single-doc-agent/debug")
async def debug_process(data: RequestData):
    text = await load_document(data.doc_url)
    stats = text_stats(text)
    logger.info("DEBUG - extracted_length=%d, lorem_count=%d, words=%d", stats["length"], stats["lorem_count"], stats["words"])
    logger.info("DEBUG - snippet (first 200 chars): %s", stats["snippet"][:200].replace("\n", "\\n"))
    return {
        "extracted_length": stats["length"],
        "lorem_count": stats["lorem_count"],
        "words": stats["words"],
        "latin_keyword_count": stats["latin_keyword_count"],
        "snippet": stats["snippet"],
    }

@singleAgentDocumentRouter.post("/single-doc-agent/test-model")
async def test_model(data: RequestData):
    if data.doc_url and (data.doc_url.startswith("http://") or data.doc_url.startswith("https://")):
        text = await load_document(data.doc_url)
    else:
        text = (data.question or "").strip()

    if not text:
        return {"error": "No input text available for model test."}

    logger.info("MODEL TEST - input length=%d", len(text))
    logger.info("MODEL TEST - preview: %s", text[:300].replace("\n", "\\n"))

    try:
        result = llm_pipeline(text, max_length=200, min_length=20, do_sample=False)
        summary = result[0].get("summary_text") if isinstance(result, list) else str(result)
        logger.info("MODEL TEST - summary preview: %s", (summary or "")[:300].replace("\n", "\\n"))
    except Exception as e:
        logger.exception("MODEL TEST - pipeline failed: %s", e)
        return {"error": "model pipeline failed", "exception": str(e)}

    try:
        prompt = text if len(text) < 4000 else text[:4000]
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = model.generate(**inputs, max_length=200)
        gen = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("MODEL TEST - direct generate preview: %s", gen[:300].replace("\n", "\\n"))
    except Exception as e:
        gen = f"generate_failed: {e}"
        logger.warning("MODEL TEST - direct generate failed: %s", e)

    return {"summary": summary, "direct_generate": gen}

@singleAgentDocumentRouter.post("/single-doc-agent/request-process")
async def request_async_process(data: RequestData):
    text = await load_document(data.doc_url)
    summary = await summarize_text(text)
    answer = await answer_question(summary, data.question)
    return {"summary": summary, "answer": answer}
