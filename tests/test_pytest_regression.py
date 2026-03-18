import pytest


@pytest.mark.regression
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_sum_smoke(a, b, expected):
    assert a + b == expected


@pytest.mark.regression
def test_example_xfail():
    pytest.xfail("Example xfail for portfolio (replace with real bug link).")

