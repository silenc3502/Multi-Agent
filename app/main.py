import os
from dotenv import load_dotenv

from anonymous_board.adapter.input.web.anonymous_board_router import anonymous_board_router
from config.database.session import Base, engine

load_dotenv()

from fastapi import FastAPI

app = FastAPI()

app.include_router(anonymous_board_router)

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
