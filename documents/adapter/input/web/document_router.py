from fastapi import APIRouter, UploadFile, File, Depends

from documents.application.factory.analyze_document_usecase_factory import get_analyze_document_usecase
from documents.application.factory.upload_file_usecase_factory import get_upload_document_usecase

documentRouter = APIRouter()

@documentRouter.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    usecase = Depends(get_upload_document_usecase)
):
    result = usecase.execute(file.file, file.filename)
    return {"url": result}

@documentRouter.post("/analysis/{document_id}")
async def analyze_document(
    document_id: int,
    usecase = Depends(get_analyze_document_usecase)
):
    result = await usecase.execute(document_id)
    return {"result": result}