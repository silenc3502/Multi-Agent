import uuid

from documents_analysis.domain.entity.document import Document
from documents_analysis.domain.repository.DocumentRepository import DocumentRepository
from documents_analysis.presentation.api.request.DocumentRequest import DocumentRequest
from utility.document_downloader import download_document, get_cache_filename
from utility.document_parser import parse_document


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    async def analyze_and_save(self, request: DocumentRequest):
        text = await self._load_and_parse_document(request.doc_url)

        document = Document(
            id=str(uuid.uuid4()),  # 유니크 ID 생성
            doc_url=request.doc_url,
        )

        await self.repository.save(document)
        return text

    async def _load_and_parse_document(self, doc_url: str) -> str:
        print(f"[DEBUG] 다운로드 시작: {doc_url}")
        content = await download_document(doc_url)

        cache_path = get_cache_filename(doc_url)
        print(f"[DEBUG] 캐시된 파일 경로: {cache_path}")

        # 디버그: 다운로드된 문서 저장
        debug_path = "debug_downloaded_document"
        with open(debug_path, "wb") as f:
            f.write(content)
        print(f"[DEBUG] 다운로드된 문서 저장: {debug_path} ({len(content)} bytes)")

        print("[DEBUG] 파싱 시작")
        text = parse_document(content, cache_path)
        print(f"[DEBUG] 파싱 완료, 길이: {len(text)} characters")

        # 파싱된 텍스트 저장
        debug_text_path = "debug_parsed_text.txt"
        with open(debug_text_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[DEBUG] 파싱된 텍스트 저장: {debug_text_path}")

        return text

