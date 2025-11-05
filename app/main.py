import os
from dotenv import load_dotenv

from documents.infrastructure.config.mysql_config import Base, engine
from documents.adapter.input.web.document_router import documentRouter
from documents_analysis.presentation.api.DocumentController import documentAnalysisRouter
from multi_agent_document.controller import multiAgentDocumentRouter

load_dotenv()

from fastapi import FastAPI
from single_agent_document.single_agent_document_controller import singleAgentDocumentRouter
from app.model_loader import download_model_if_needed

download_model_if_needed()

app = FastAPI()

# Test
app.include_router(singleAgentDocumentRouter)
app.include_router(multiAgentDocumentRouter)
app.include_router(documentAnalysisRouter)

# Real
app.include_router(documentRouter, prefix="/documents")

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
