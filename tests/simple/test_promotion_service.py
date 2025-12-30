from datetime import datetime, timedelta

from simple.promotion_service import PromotionService


def test_promotion_active():
    start = datetime(2025, 12, 30, 9, 0, 0)
    end = datetime(2025, 12, 30, 18, 0, 0)
    promo = PromotionService(0.2, start, end)

    # 이벤트 활성 시간
    current = datetime(2025, 12, 30, 10, 0, 0)
    assert promo.is_active(current) is True
    assert promo.apply_discount(100, current) == 80.0


def test_promotion_inactive_before():
    start = datetime(2025, 12, 30, 9, 0, 0)
    end = datetime(2025, 12, 30, 18, 0, 0)
    promo = PromotionService(0.2, start, end)

    # 이벤트 시작 전
    current = datetime(2025, 12, 30, 8, 0, 0)
    assert promo.is_active(current) is False
    assert promo.apply_discount(100, current) == 100.0


def test_promotion_inactive_after():
    start = datetime(2025, 12, 30, 9, 0, 0)
    end = datetime(2025, 12, 30, 18, 0, 0)
    promo = PromotionService(0.2, start, end)

    # 이벤트 종료 후
    current = datetime(2025, 12, 30, 19, 0, 0)
    assert promo.is_active(current) is False
    assert promo.apply_discount(100, current) == 100.0
