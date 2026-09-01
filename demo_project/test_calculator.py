import pytest

from calculator import add, subtract, divide


def test_add() -> None:
    assert add(2, 3) == 5


def test_subtract() -> None:
    assert subtract(5, 3) == 2


def test_divide() -> None:
    assert divide(6, 3) == 2


def test_divide_returns_float() -> None:
    assert divide(1, 2) == 0.5


def test_divide_negative() -> None:
    assert divide(-9, 3) == -3
    assert divide(9, -3) == -3


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ValueError):
        divide(1, 0)


def test_divide_zero_by_zero_raises() -> None:
    with pytest.raises(ValueError):
        divide(0, 0)


def test_divide_zero_numerator() -> None:
    assert divide(0, 5) == 0
