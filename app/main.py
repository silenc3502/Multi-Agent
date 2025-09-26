import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from single_agent_document.single_agent_document_controller import singleAgentDocumentRouter
from app.model_loader import download_model_if_needed

download_model_if_needed()

app = FastAPI()
app.include_router(singleAgentDocumentRouter)

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    uvicorn.run(app, host=host, port=port)
