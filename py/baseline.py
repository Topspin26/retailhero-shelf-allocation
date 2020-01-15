import sys
from typing import NamedTuple, Tuple, List

# from base import Item, Rectangle, create_empty_matrix
# ----------copy from base.py---------- #
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
# ----------copy from base.py---------- #


def run():
    n, k, m, h, w, d0, items = read_input(sys.stdin)

    cat2items: List[List[Item]] = []
    for i in range(k):
        cat2items.append([])

    for item in items:
        cat2items[item.cat - 1].append(item)

    '''
    for each category sort items by cost in descending order (and secondary sort by brand for reproducibility)
    '''
    for i in range(k):
        cat2items[i] = sorted(cat2items[i], key=lambda x: (-x.c, x.brand))

    '''
    calculate for each triple (cat - category, h - rectangle height, w - rectangle width):
        cat_score[cat][h][w] - estimate of score using greedy filling approach
        cat_score_items[cat][h][w] - ordered list of items for shelf filling 
    '''
    cat_score: List[List[List[float]]] = []
    cat_score_items: List[List[List[List[Item]]]] = []
    for i in range(k):
        cat_score_i = []
        cat_score_i_items = []
        for hh in range(h + 1):
            cat_score_i.append([0] * (w + 1))
            cat_score_i_items.append([None] * (w + 1))

        for hh in range(1, h + 1):
            for ww in range(1, w + 1):
                simple_brand_score = 0
                n_real = min(len(cat2items[i]), ww * hh)
                for j in range(n_real):
                    simple_brand_score += cat2items[i][j].c

                cat_score_i[hh][ww] = simple_brand_score + d0 * (n_real / (w * h))**0.5
                # group(sort) choosed items by brand (and secondary sort by cost for reproducibility)
                cat_score_i_items[hh][ww] = sorted(cat2items[i][:n_real].copy(), key=lambda x: (x.brand, -x.c))
        cat_score.append(cat_score_i)
        cat_score_items.append(cat_score_i_items)

    '''
    DP(Dynamic Programming) part to find optimal rectangle size for each category
        c[i][j] - best estimate of score for shelf size = (h x j) if we used only categories 1..i
        c_best[i][j] - for shelf size = (h x j) stores best rectangle (w_cat, h_cat) for i-th category 
                       (is necessary for fast answer recovering)
    '''
    c: List[List[float]] = []
    c_best: List[List[Rectangle]] = []
    for i in range(k + 1):
        c.append([0] * (w + 1))
        c_best.append([Rectangle(0, 0)] * (w + 1))

    for i in range(k):
        for j in range(w + 1):
            n_items_in_cat_i = len(cat2items[i])
            # brute force all possible rectangle sizes for i-th category
            for w_cat in range(min(n_items_in_cat_i, w - j) + 1):
                for h_cat in range(h + 1):
                    if h_cat * w_cat > n_items_in_cat_i:
                        break
                    new_score = c[i][j] + cat_score[i][h_cat][w_cat]
                    if c[i + 1][j + w_cat] < new_score:
                        c[i + 1][j + w_cat] = new_score
                        c_best[i + 1][j + w_cat] = Rectangle(w_cat, h_cat)

    '''
    Answer recovering part using c_best matrix
    '''
    res = create_empty_matrix(h, w)
    i, j = k, w
    while i > 0:
        rectangle = c_best[i][j]
        cc = 0
        for u in range(rectangle.h):
            for q in range(j - rectangle.w, j):
                res[u][q] = cat_score_items[i - 1][rectangle.h][rectangle.w][cc]
                cc += 1
        i -= 1
        j -= rectangle.w

    for i in range(h):
        print(' '.join([str(e.ind) for e in res[i]]))


def read_input(fin) -> Tuple[int, int, int, int, int, int, List[Item]]:
    n, k, m, h, w, d0 = map(int, fin.readline().strip().split())
    items = []
    for i in range(n):
        ti, bi, ci = map(int, fin.readline().strip().split())
        items.append(Item((i + 1), ti, bi, ci))
    return n, k, m, h, w, d0, items


if __name__ == '__main__':
    run()
