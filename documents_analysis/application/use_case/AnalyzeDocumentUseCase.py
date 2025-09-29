from documents_analysis.domain.service.DocumentService import DocumentService


class AnalyzeDocumentUseCase:
    def __init__(self, service: DocumentService):
        self.service = service

    async def execute(self, request):
        return await self.service.analyze_and_save(request)
