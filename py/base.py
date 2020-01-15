from typing import NamedTuple, List


class Item(NamedTuple):
    ind: int
    cat: int
    brand: int
    c: int


class Rectangle(NamedTuple):
    w: int
    h: int


def create_empty_matrix(h: int, w: int) -> List[List[Item]]:
    return [[Item(0, -1, -1, 0) for _ in range(w)] for _ in range(h)]
