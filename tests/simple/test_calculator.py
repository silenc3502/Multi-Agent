import pytest

from simple.calculator import divide, add


# 1) 덧셈 테스트
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# 2) 나눗셈 테스트
def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

# 3) 예외 테스트
def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)

    assert str(exc_info.value) == "Cannot divide by zero"
