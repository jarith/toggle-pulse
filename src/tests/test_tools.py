from python_starter_template.tools import add, sub


def test_add() -> None:
    assert add(1, 2) == 3


def test_sub() -> None:
    assert sub(1, 2) == -1
