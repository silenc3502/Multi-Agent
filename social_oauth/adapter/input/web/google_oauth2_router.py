import uuid
from fastapi import APIRouter, Response, Request, Cookie
from fastapi.responses import RedirectResponse

from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from config.redis_config import get_redis
from social_oauth.application.usecase.google_oauth2_usecase import GoogleOAuth2UseCase
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service

authentication_router = APIRouter()
service = GoogleOAuth2Service()
account_repository = AccountRepositoryImpl()
account_usecase = AccountUseCase(account_repository)
google_usecase = GoogleOAuth2UseCase(service)

redis_client = get_redis()


@authentication_router.get("/google")
async def redirect_to_google():
    url = google_usecase.get_authorization_url()
    print("[DEBUG] Redirecting to Google:", url)
    return RedirectResponse(url)


# Google에게 요청이 날아감.
# 그런데 Google Cloud에 가서 redirect uri에 설정해 놓은 것이 있음.
# 로그인이 완료되는 순간 알아서 Google Cloud에 등록한 redirect uri로 날아감
# 근데 그 주소가 우리는 localhost:33333/authentication/google/redirect 였음.
# 그렇기 때문에 구글 로그인이 성공하면 아래 Controller (Router)가 동작하게 됨.
@authentication_router.get("/google/redirect")
async def process_google_redirect(
    response: Response,
    code: str,
    state: str | None = None
):
    print("[DEBUG] /google/redirect called")
    print("code:", code)
    print("state:", state)

    result = google_usecase.fetch_user_profile(code, state or "")
    profile = result["profile"]
    access_token = result["access_token"]
    print("profile:", profile)

    # 계정 생성/조회
    account = account_usecase.create_or_get_account(
        profile.get("email"),
        profile.get("name")
    )

    # session_id 생성
    session_id = str(uuid.uuid4())
    print("[DEBUG] Generated session_id:", session_id)

    # Redis에 session 저장 (1시간 TTL)
    redis_client.set(session_id, access_token.access_token, ex=3600)
    print("[DEBUG] Session saved in Redis:", redis_client.exists(session_id))

    # 브라우저 쿠키 발급
    # 해당 부분도 .env.local 혹은 .env.production 등으로 관리 되어야 함.
    redirect_response = RedirectResponse("http://localhost:3000")
    redirect_response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )
    print("[DEBUG] Cookie set in RedirectResponse directly")
    return redirect_response

@authentication_router.get("/status")
async def auth_status(request: Request, session_id: str | None = Cookie(None)):
    print("[DEBUG] /status called")

    # 모든 요청 헤더 출력
    print("[DEBUG] Request headers:", request.headers)

    # 쿠키 확인
    print("[DEBUG] Received session_id cookie:", session_id)

    if not session_id:
        print("[DEBUG] No session_id received. Returning logged_in: False")
        return {"logged_in": False}

    exists = redis_client.exists(session_id)
    print("[DEBUG] Redis has session_id?", exists)

    return {"logged_in": bool(exists)}
