import os
from dotenv import load_dotenv

from anonymous_board.adapter.input.web.anonymous_board_router import anonymous_board_router
from config.database.session import Base, engine
from social_oauth.adapter.input.web.google_oauth2_router import authentication_router

load_dotenv()

from fastapi import FastAPI

app = FastAPI()

app.include_router(anonymous_board_router, prefix="/board")
app.include_router(authentication_router, prefix="/authentication")

# 앱 실행
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
