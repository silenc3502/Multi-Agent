import pytest
from kakao_authentication.domain.value_objects.kakao_email import KakaoEmail
from kakao_authentication.domain.value_objects.kakao_nickname import KakaoNickname
from kakao_authentication.domain.value_objects.kakao_user_id import KakaoUserId
from kakao_authentication.domain.kakao_user import KakaoUser


# 정상 생성
def test_kakao_user_creation():
    user_id = KakaoUserId(1)
    email = KakaoEmail("test@example.com")
    nickname = KakaoNickname("nickname")

    user = KakaoUser(user_id=user_id, email=email, nickname=nickname)

    assert user.user_id.value == 1
    assert user.email.value == "test@example.com"
    assert user.nickname.value == "nickname"


# 잘못된 이메일 입력 시 ValueError 발생
def test_kakao_user_invalid_email():
    user_id = KakaoUserId(1)
    with pytest.raises(ValueError):
        email = KakaoEmail("invalid-email")
        nickname = KakaoNickname("nickname")
        KakaoUser(user_id=user_id, email=email, nickname=nickname)


# 잘못된 닉네임 입력 시 ValueError 발생
def test_kakao_user_invalid_nickname():
    user_id = KakaoUserId(1)
    email = KakaoEmail("test@example.com")
    with pytest.raises(ValueError):
        nickname = KakaoNickname("")  # 빈 문자열
        KakaoUser(user_id=user_id, email=email, nickname=nickname)


# 잘못된 사용자 ID 입력 시 ValueError 발생
def test_kakao_user_invalid_user_id():
    email = KakaoEmail("test@example.com")
    nickname = KakaoNickname("nickname")
    with pytest.raises(ValueError):
        user_id = KakaoUserId(0)
        KakaoUser(user_id=user_id, email=email, nickname=nickname)
