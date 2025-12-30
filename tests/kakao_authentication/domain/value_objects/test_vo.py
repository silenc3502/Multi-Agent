import pytest
from kakao_authentication.domain.value_objects.kakao_access_token import KakaoAccessToken
from kakao_authentication.domain.value_objects.kakao_authorization_url import KakaoAuthorizationUrl
from kakao_authentication.domain.value_objects.kakao_email import KakaoEmail
from kakao_authentication.domain.value_objects.kakao_nickname import KakaoNickname
from kakao_authentication.domain.value_objects.kakao_refresh_token import KakaoRefreshToken
from kakao_authentication.domain.value_objects.kakao_user_id import KakaoUserId

# KakaoAccessToken
def test_access_token_valid():
    token = KakaoAccessToken("abc123")
    assert token.value == "abc123"

def test_access_token_empty():
    with pytest.raises(ValueError):
        KakaoAccessToken("")

# KakaoAuthorizationUrl
def test_authorization_url_build():
    url = KakaoAuthorizationUrl("client_id", "https://example.com/callback")
    assert "client_id=client_id" in str(url)
    assert "redirect_uri=https://example.com/callback" in str(url)
    assert url.build().startswith("https://kauth.kakao.com/oauth/authorize")

def test_authorization_url_missing_params():
    with pytest.raises(ValueError):
        KakaoAuthorizationUrl("", "https://example.com")

    with pytest.raises(ValueError):
        KakaoAuthorizationUrl("client_id", "")

# KakaoEmail
def test_email_valid():
    email = KakaoEmail("test@example.com")
    assert email.value == "test@example.com"

def test_email_invalid():
    with pytest.raises(ValueError):
        KakaoEmail("invalid-email")

# KakaoNickname
def test_nickname_valid():
    nick = KakaoNickname("  nick  ")
    assert nick.value == "nick"

def test_nickname_empty_or_long():
    with pytest.raises(ValueError):
        KakaoNickname("")
    with pytest.raises(ValueError):
        KakaoNickname(" " * 5)
    with pytest.raises(ValueError):
        KakaoNickname("a" * 21)

# KakaoRefreshToken
def test_refresh_token_valid():
    token = KakaoRefreshToken("refresh123")
    assert token.value == "refresh123"

def test_refresh_token_empty():
    with pytest.raises(ValueError):
        KakaoRefreshToken("")

# KakaoUserId
def test_user_id_valid():
    user_id = KakaoUserId(10)
    assert user_id.value == 10

def test_user_id_invalid():
    with pytest.raises(ValueError):
        KakaoUserId(0)
    with pytest.raises(ValueError):
        KakaoUserId(-1)
