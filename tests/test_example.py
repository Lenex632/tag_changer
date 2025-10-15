import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize('a, b, expected', [
    (1, 2, 3),
    (2, 3, 6),
    (-1, 1, 0),
])
def test_math(a, b, expected):
    assert add(a, b) == expected

