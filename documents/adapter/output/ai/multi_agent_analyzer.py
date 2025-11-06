# multi_agent_analyzer_token_chunks.py
from typing import Annotated, List
from langgraph.graph import StateGraph
from transformers import pipeline, AutoTokenizer
import asyncio
import fitz  # PyMuPDF
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# LangGraph 호환 상태 스키마 (타입으로 제공)
# ---------------------------
class MyStateSchema:
    bullet_summary_done: bool = False
    abstract_summary_done: bool = False
    casual_summary_done: bool = False
    final_summary_done: bool = False
    answer_generated: bool = False

# ---------------------------
# PDF 읽기 유틸
# ---------------------------
def read_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return "\n".join(pages).strip()

# ---------------------------
# 토큰 단위 chunking (토크나이저 사용)
# - 안전하게 모델의 max_input_tokens를 넘기지 않도록 자른다.
# - special tokens 고려 -> margin으로 여유 둠
# ---------------------------
class TokenChunker:
    def __init__(self, tokenizer, max_input_tokens: int = 1024, margin_tokens: int = 50):
        """
        max_input_tokens: 모델 encoder max length (e.g., bart-large-cnn ~1024)
        margin_tokens: 여유 토큰 수 (프롬프트/특수문자/버퍼용)
        """
        self.tokenizer = tokenizer
        self.max_tokens = max_input_tokens
        self.margin = margin_tokens
        # 실제로 chunk에 사용할 최대 토큰 수
        self.chunk_size = max(64, self.max_tokens - self.margin)

    def chunk_text(self, text: str) -> List[str]:
        """
        Returns list of text chunks, each decoded back to text, each chunk token length <= chunk_size
        """
        # 토큰화(정수 id 리스트)
        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        total = len(token_ids)
        if total == 0:
            return []
        num_chunks = math.ceil(total / self.chunk_size)
        for i in range(num_chunks):
            start = i * self.chunk_size
            end = start + self.chunk_size
            chunk_ids = token_ids[start:end]
            # 디코드할 때 special tokens 생략
            chunk_text = self.tokenizer.decode(chunk_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            chunks.append(chunk_text.strip())
        return chunks

# ---------------------------
# Analyzer: tokenizer 기반 chunk 요약 + final 합치기 + QA
# ---------------------------
class MultiAgentAnalyzer:
    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        device: int = -1,  # CPU:-1, GPU:0
        encoder_max_tokens: int | None = None,
        max_concurrent_workers: int = 3
    ):
        """
        encoder_max_tokens: model encoder max tokens, None이면 기본값 1024 사용
        """
        logger.info("Initializing tokenizer and summarization pipeline...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.summarizer = pipeline("summarization", model=model_name, tokenizer=self.tokenizer, device=device)
        # 모델의 encoder max tokens (기본값 1024)
        self.encoder_max_tokens = encoder_max_tokens or 1024
        self.chunker = TokenChunker(self.tokenizer, max_input_tokens=self.encoder_max_tokens, margin_tokens=50)
        # 동시성 제어: thread pool 호출 폭주 방지
        self.semaphore = asyncio.Semaphore(max_concurrent_workers)

    async def _summarize_single_chunk(self, prompt: str, max_length: int = 250, min_length: int = 20) -> str:
        loop = asyncio.get_event_loop()
        # 파이프라인 호출을 thread executor로 감싸서 비동기에서 안전 사용
        def sync_call():
            # try/except로 safety net (예상치 못한 model error시 fallback)
            try:
                out = self.summarizer(prompt, max_length=max_length, min_length=min_length, do_sample=False)
                # pipeline은 리스트를 반환
                if isinstance(out, list) and len(out) > 0 and isinstance(out[0], dict):
                    return out[0].get("summary_text", "").strip()
                # fallback
                return str(out).strip()
            except Exception as e:
                logger.exception("Summarizer failed on chunk: %s", e)
                # 안전하게 입력을 잘라서 다시 시도 (토큰량 강제 제한)
                encoded = self.tokenizer.encode(prompt, truncation=True, max_length=self.chunker.chunk_size)
                truncated = self.tokenizer.decode(encoded, skip_special_tokens=True)
                out2 = self.summarizer(truncated, max_length=max_length, min_length=min_length, do_sample=False)
                return out2[0].get("summary_text", "").strip()

        # semaphore로 동시성 제어
        async with self.semaphore:
            result = await loop.run_in_executor(None, sync_call)
        return result

    async def summarize_token_chunks(self, text: str, prompt_type: str) -> str:
        """
        prompt_type: "bullet", "abstract", "casual"
        returns: concatenated chunk summaries (joined by newline)
        """
        if not text:
            return ""

        chunks = self.chunker.chunk_text(text)
        logger.info("Text split into %d chunks (token-based).", len(chunks))
        tasks = []
        for chunk in chunks:
            if prompt_type == "bullet":
                prompt = f"Summarize the following text in concise bullet points (use '-' or '*' per bullet):\n\n{chunk}"
                max_len = 180
                min_len = 10
            elif prompt_type == "abstract":
                prompt = f"Write an academic-style abstract for the following text (single-paragraph):\n\n{chunk}"
                max_len = 200
                min_len = 40
            elif prompt_type == "casual":
                prompt = f"Write a short, casual, easy-to-understand summary for general readers:\n\n{chunk}"
                max_len = 160
                min_len = 20
            else:
                prompt = chunk
                max_len = 150
                min_len = 20

            tasks.append(self._summarize_single_chunk(prompt, max_length=max_len, min_length=min_len))

        # chunk별 요약을 병렬 실행 (세마포어로 동시성 제한)
        chunk_summaries = await asyncio.gather(*tasks)
        # 정리: 중복 공백 제거
        cleaned = [s for s in (c.strip() for c in chunk_summaries) if s]
        return "\n".join(cleaned)

    async def generate_final_summary(self, bullet: str, abstract: str, casual: str) -> str:
        prompt = (
            "Merge the following summaries into a single, clear comprehensive overview. "
            "Keep it concise (one or two paragraphs), avoid repeating phrases, and keep factual tone.\n\n"
            f"Bullet Summary:\n{bullet}\n\nAbstract:\n{abstract}\n\nCasual Summary:\n{casual}\n"
        )
        return await self._summarize_single_chunk(prompt, max_length=300, min_length=80)

    async def generate_qa(self, text: str, num_qa: int = 6) -> str:
        """
        Generate potential user Q&A pairs from the full text.
        """
        # 안전: 길면 chunk 하나로 줄여서 진행 (QA는 전체 내용의 요약으로 생성)
        # 먼저 간단한 doc-level summary (short)
        short_summary = await self._summarize_single_chunk(
            f"Summarize the following text in 2-3 sentences:\n\n{text}", max_length=120, min_length=30
        )
        prompt = (
            f"Based on the summary and content below, generate up to {num_qa} useful user questions and short answers. "
            "Format each as: Q: ... A: ...\n\n"
            f"Short summary:\n{short_summary}\n\nContent excerpt:\n{text[:4000]}"  # 앞 부분만 넣음 (안정성)
        )
        return await self._summarize_single_chunk(prompt, max_length=300, min_length=60)

    async def run(self, local_path: str):
        # 1) PDF 읽기
        text_content = read_pdf(local_path)
        if not text_content:
            raise ValueError("PDF content is empty or not readable.")

        # 2) LangGraph compatible StateGraph (type + reducer)
        graph = StateGraph(Annotated[MyStateSchema, "reducer"])
        state = MyStateSchema()

        # 3) Parallel chunked summaries
        bullet_task = self.summarize_token_chunks(text_content, "bullet")
        abstract_task = self.summarize_token_chunks(text_content, "abstract")
        casual_task = self.summarize_token_chunks(text_content, "casual")

        bullet_summary, abstract_summary, casual_summary = await asyncio.gather(
            bullet_task, abstract_task, casual_task
        )
        state.bullet_summary_done = True
        state.abstract_summary_done = True
        state.casual_summary_done = True

        # 4) Final merged summary
        final_summary = await self.generate_final_summary(bullet_summary, abstract_summary, casual_summary)
        state.final_summary_done = True

        # 5) QA generation (uses short summary + excerpt)
        answer = await self.generate_qa(text_content, num_qa=6)
        state.answer_generated = True

        # 6) 결과
        state_dict = {
            "bullet_summary_done": state.bullet_summary_done,
            "abstract_summary_done": state.abstract_summary_done,
            "casual_summary_done": state.casual_summary_done,
            "final_summary_done": state.final_summary_done,
            "answer_generated": state.answer_generated,
        }

        return {
            "summaries": {
                "bullet": bullet_summary,
                "abstract": abstract_summary,
                "casual": casual_summary,
            },
            "final_summary": final_summary,
            "answer": answer,
            "state": state_dict
        }

# ---------------------------
# 사용 예시
# ---------------------------
# if __name__ == "__main__":
#     import asyncio
#     analyzer = MultiAgentAnalyzer(device=-1)  # CPU
#     res = asyncio.run(analyzer.run("downloaded_docs/sample.pdf"))
#     from pprint import pprint
#     pprint(res)
