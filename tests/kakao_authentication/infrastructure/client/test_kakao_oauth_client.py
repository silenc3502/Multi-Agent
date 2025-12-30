import pytest
from unittest.mock import patch, Mock
from kakao_authentication.infrastructure.client.kakao_oauth_client import KakaoOAuthClient
from kakao_authentication.domain.value_objects.kakao_access_token import KakaoAccessToken
from kakao_authentication.domain.kakao_user import KakaoUser

# get_access_token 테스트
def test_get_access_token_success():
    mock_response = Mock()
    mock_response.json.return_value = {"access_token": "abc123"}
    mock_response.raise_for_status = Mock()

    client = KakaoOAuthClient()

    with patch("kakao_authentication.infrastructure.client.kakao_oauth_client.requests.post", return_value=mock_response) as mock_post:
        token = client.get_access_token("auth_code")
        mock_post.assert_called_once()  # requests.post 호출 확인
        assert isinstance(token, KakaoAccessToken)
        assert token.value == "abc123"

# get_user_info 테스트
def test_get_user_info_success():
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 123,
        "kakao_account": {"email": "test@example.com"},
        "properties": {"nickname": "nickname"}
    }
    mock_response.raise_for_status = Mock()

    client = KakaoOAuthClient()
    token = KakaoAccessToken("abc123")

    with patch("kakao_authentication.infrastructure.client.kakao_oauth_client.requests.get", return_value=mock_response) as mock_get:
        user = client.get_user_info(token)
        mock_get.assert_called_once()  # requests.get 호출 확인
        assert isinstance(user, KakaoUser)
        assert user.user_id.value == 123
        assert user.email.value == "test@example.com"
        assert user.nickname.value == "nickname"

# HTTP 오류 시 예외 처리 테스트
def test_get_access_token_http_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")

    client = KakaoOAuthClient()

    with patch("kakao_authentication.infrastructure.client.kakao_oauth_client.requests.post", return_value=mock_response):
        with pytest.raises(Exception):
            client.get_access_token("auth_code")
