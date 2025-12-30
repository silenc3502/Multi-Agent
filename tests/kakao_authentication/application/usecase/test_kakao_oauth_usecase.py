import pytest
from unittest.mock import Mock, patch
from kakao_authentication.application.usecase.kakao_oauth_usecase import KakaoOAuthUseCase
from kakao_authentication.domain.kakao_user import KakaoUser
from kakao_authentication.domain.value_objects.kakao_access_token import KakaoAccessToken
from kakao_authentication.domain.value_objects.kakao_email import KakaoEmail
from kakao_authentication.domain.value_objects.kakao_nickname import KakaoNickname
from kakao_authentication.domain.value_objects.kakao_user_id import KakaoUserId

def test_get_authorization_url_mocked_env():
    mock_port = Mock()
    with patch("kakao_authentication.application.usecase.kakao_oauth_usecase.KAKAO_CLIENT_ID", "test_client_id"), \
         patch("kakao_authentication.application.usecase.kakao_oauth_usecase.KAKAO_REDIRECT_URI", "https://test.com/callback"):

        usecase = KakaoOAuthUseCase(mock_port)
        url = usecase.get_authorization_url()

        assert "client_id=test_client_id" in url
        assert "redirect_uri=https://test.com/callback" in url

def test_get_kakao_user():
    mock_port = Mock()

    # Mock AccessToken
    mock_access_token = KakaoAccessToken("access123")
    mock_port.get_access_token.return_value = mock_access_token

    # Mock KakaoUser
    mock_user = KakaoUser(
        user_id=KakaoUserId(1),
        email=KakaoEmail("test@example.com"),
        nickname=KakaoNickname("nickname")
    )
    mock_port.get_user_info.return_value = mock_user

    usecase = KakaoOAuthUseCase(mock_port)
    result = usecase.get_kakao_user("auth_code")

    # 포트 호출 검증
    mock_port.get_access_token.assert_called_once_with("auth_code")
    mock_port.get_user_info.assert_called_once_with(mock_access_token)

    # 반환값 검증
    assert result["access_token"] == "access123"
    assert result["user"].user_id.value == 1
    assert result["user"].email.value == "test@example.com"
    assert result["user"].nickname.value == "nickname"
