from documents.domain.entity.document import Document

class AnalyzeDocumentUseCase:
    def __init__(self, document_repo, storage_adapter, analyzer):
        self.document_repo = document_repo
        self.storage_adapter = storage_adapter
        self.analyzer = analyzer

    async def execute(self, document_id: int):
        # DB에서 Document 조회
        document: Document = self.document_repo.find_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id={document_id} not found")

        s3_url = str(document.path.s3_url)
        print(f"Downloading from S3: {s3_url}")

        # S3에서 로컬 다운로드
        local_path = await self.storage_adapter.download_file(s3_url)
        print(f"Downloaded to: {local_path}")

        # 멀티에이전트 분석 실행
        result = await self.analyzer.run(local_path)
        return result
