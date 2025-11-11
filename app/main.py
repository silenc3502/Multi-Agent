import os
from dotenv import load_dotenv

from anonymous_board.controller.anonymous_board_controller import anonymous_board_controller
from config.mysql_config import Base, engine

load_dotenv()

from fastapi import FastAPI

app = FastAPI()

app.include_router(anonymous_board_controller)

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
