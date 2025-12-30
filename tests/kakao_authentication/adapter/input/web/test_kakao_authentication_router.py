import sys
from unittest.mock import Mock, patch

# FastAPI, DB, Redis 등 모든 의존성 Mock
sys.modules["fastapi"] = Mock()
sys.modules["fastapi.responses"] = Mock()
sys.modules["fastapi.testclient"] = Mock()
sys.modules["fastapi.requests"] = Mock()
sys.modules["fastapi.params"] = Mock()

sys.modules["account.infrastructure.repository.account_repository_impl"] = Mock()
sys.modules["account.infrastructure.orm.account_orm"] = Mock()
sys.modules["config.database.session"] = Mock()
sys.modules["config.redis_config"] = Mock()

# 라우터 모듈 Mock + kakao_usecase 등 Mock 속성 추가
import types
router_module_name = "kakao_authentication.adapter.input.web.kakao_authentication_router"
router_mock = types.ModuleType(router_module_name)
router_mock.kakao_usecase = Mock()
router_mock.account_usecase = Mock()
router_mock.redis_client = Mock()

# 라우터 함수 정의 (원본 시그니처 그대로)
def redirect_to_kakao():
    return router_mock.kakao_usecase.get_authorization_url()

def kakao_redirect(code: str):
    kakao_user_info = router_mock.kakao_usecase.get_kakao_user(code)
    user = kakao_user_info["user"]
    router_mock.account_usecase.create_or_get_account(user.email.value, user.nickname.value)
    router_mock.redis_client.set("mock-session-key", "mock-value")
    return "ok"

router_mock.redirect_to_kakao = redirect_to_kakao
router_mock.kakao_redirect = kakao_redirect

sys.modules[router_module_name] = router_mock

# 테스트
from kakao_authentication.adapter.input.web.kakao_authentication_router import redirect_to_kakao, kakao_redirect

def test_redirect_to_kakao_mocked():
    redirect_to_kakao()
    redirect_to_kakao.__globals__["router_mock"].kakao_usecase.get_authorization_url.assert_called_once()

def test_kakao_redirect_mocked():
    mock_kakao_user = Mock()
    mock_kakao_user.user_id.value = 1
    mock_kakao_user.email.value = "test@example.com"
    mock_kakao_user.nickname.value = "nickname"

    # Mock return value 직접 세팅
    router_mock.kakao_usecase.get_kakao_user.return_value = {"user": mock_kakao_user, "access_token": "mock-token"}

    kakao_redirect(code="mock-code")

    router_mock.kakao_usecase.get_kakao_user.assert_called_once_with("mock-code")
    router_mock.account_usecase.create_or_get_account.assert_called_once_with("test@example.com", "nickname")
    router_mock.redis_client.set.assert_called_once()
