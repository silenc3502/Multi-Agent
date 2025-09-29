from fastapi import APIRouter

from documents_analysis.application.use_case.AnalyzeDocumentUseCase import AnalyzeDocumentUseCase
from documents_analysis.domain.service.DocumentService import DocumentService
from documents_analysis.infrastructure.repository.InMemoryDocumentRepository import InMemoryDocumentRepository
from documents_analysis.presentation.api.request.DocumentRequest import DocumentRequest

documentRouter = APIRouter()


@documentRouter.post("/document/analyze")
async def analyze_document(request: DocumentRequest):
    repository = InMemoryDocumentRepository()
    service = DocumentService(repository)
    use_case = AnalyzeDocumentUseCase(service)

    result = await use_case.execute(request)
    return {"result": result}