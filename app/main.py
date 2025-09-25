import os
from fastapi import FastAPI

from single_agent_document.single_agent_document_controller import singleAgentDocumentRouter

app = FastAPI()

app.include_router(singleAgentDocumentRouter)

# 앱 실행
if __name__ == "__main__":
    import uvicorn

    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))

    uvicorn.run(app, host=host, port=port)