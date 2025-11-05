from fastapi import APIRouter, UploadFile, File, Depends

from documents.application.factory.upload_file_usecase_factory import get_upload_document_usecase

documentRouter = APIRouter()

@documentRouter.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    usecase = Depends(get_upload_document_usecase)
):
    result = usecase.execute(file.file, file.filename)
    return {"url": result}
