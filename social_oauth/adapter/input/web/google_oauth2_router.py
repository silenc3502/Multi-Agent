import uuid

from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse

from config.redis_config import get_redis
from social_oauth.application.usecase.google_oauth2_usecase import GoogleOAuth2UseCase
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service

authentication_router = APIRouter()
service = GoogleOAuth2Service()
usecase = GoogleOAuth2UseCase(service)
redis_client = get_redis()

@authentication_router.get("/google")
async def redirect_to_google():
    url = usecase.get_authorization_url()
    return RedirectResponse(url)

@authentication_router.get("/google/redirect")
async def process_google_redirect(
    response: Response,
    code: str,
    state: str | None = None
):

    # code -> access token
    access_token = usecase.login_and_fetch_user(state or "", code)

    # session_id 생성
    session_id = str(uuid.uuid4())

    # Redis에 session 저장 (1시간 TTL)
    redis_client.set(session_id, access_token.access_token, ex=3600)

    # 브라우저 쿠키 발급
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # HTTPS 환경이면 True
        max_age=3600
    )

    # 프론트 리다이렉트
    return RedirectResponse("http://localhost:3000")
