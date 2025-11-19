from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from documents.adapter.input.web.request.register_document_request import RegisterDocumentRequest
from documents.application.usecase.document_usecase import DocumentUseCase

documents_router = APIRouter(tags=["documents"])

document_usecase = DocumentUseCase.getInstance()

from account.adapter.input.web.session_helper import get_current_user

@documents_router.post("/register")
async def register_document(
    payload: RegisterDocumentRequest,
    user_id: int = Depends(get_current_user)
):
    doc = document_usecase.register_document(
        file_name=payload.file_name,
        s3_key=payload.s3_key,
        uploader_id=user_id
    )
    return JSONResponse({
        "id": doc.id,
        "file_name": doc.file_name,
        "s3_key": doc.s3_key,
        "uploader_id": doc.uploader_id
    })
@documents_router.get("/list")
async def list_documents():
    return document_usecase.list_documents()