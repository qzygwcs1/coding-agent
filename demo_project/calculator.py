def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


def divide(a: float, b: float) -> float:
    """返回 a 除以 b 的结果。

    当除数 b 为零时抛出 ValueError。
    """
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
