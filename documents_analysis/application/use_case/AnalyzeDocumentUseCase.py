from documents_analysis.domain.entity.document import DocumentAnalysisResult
from documents_analysis.domain.service.AbstractSummaryService import AbstractSummaryService
from documents_analysis.domain.service.AnswerService import AnswerService
from documents_analysis.domain.service.BulletSummaryService import BulletSummaryService
from documents_analysis.domain.service.CasualSummaryService import CasualSummaryService
from documents_analysis.domain.service.ConsensusSummaryService import ConsensusSummaryService
from documents_analysis.domain.service.DocumentService import DocumentService
from documents_analysis.presentation.api.request.DocumentRequest import DocumentRequest
from utility.id_generator import generate_uuid


class AnalyzeDocumentUseCase:
    def __init__(self, service: DocumentService):
        self.document_service = service
        self.abstract_service = AbstractSummaryService()
        self.bullet_service = BulletSummaryService()
        self.casual_service = CasualSummaryService()
        self.consensus_service = ConsensusSummaryService()
        self.answer_service = AnswerService()

    async def execute(self, request: DocumentRequest):
        # 1. 문서 로드, 파싱, 파일 타입 추출
        text, file_type = await self.document_service._load_and_parse_document(request.doc_url)

        # 2. 요약 처리
        abstract_summary = await self.abstract_service.summarize(text)
        casual_summary = await self.casual_service.summarize(text)
        bullet_summary = await self.bullet_service.summarize(text)
        final_summary = await self.consensus_service.summarize(
            [bullet_summary, abstract_summary, casual_summary]
        )

        # 3. 질문에 대한 답변 생성
        answer = await self.answer_service.answer(final_summary, request.question)

        # 4. DocumentAnalysisResult 생성 및 저장
        result = DocumentAnalysisResult(
            id=generate_uuid(),
            doc_url=request.doc_url,
            file_type=file_type,
            bullet_summary=bullet_summary,
            abstract_summary=abstract_summary,
            casual_summary=casual_summary,
            final_summary=final_summary,
            question=request.question,
            answer=answer
        )

        await self.document_service.create(result)

        return result

