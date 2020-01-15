import math
from typing import List
from base import Item


def calculate_final_score(a: List[List[Item]], h: int, w: int, n_cat: int, d0: int) -> float:
    cat_score = calculate_cat_score(a, h, w, n_cat, d0)
    if cat_score == -1:
        return -1
    brand_score = calculate_brand_score(a, h, w)
    score = cat_score + brand_score
    return score


def calculate_cat_score(a: List[List[Item]], h: int, w: int, n_cat: int, d0: int) -> float:
    min_h, max_h, min_w, max_w, cnt = [], [], [], [], []
    for i in range(n_cat):
        min_h.append(h + 1)
        max_h.append(-1)
        min_w.append(w + 1)
        max_w.append(-1)
        cnt.append(0)

    for i in range(h):
        for j in range(w):
            # if cell is not empty
            if a[i][j].cat != -1:
                min_h[a[i][j].cat - 1] = min(min_h[a[i][j].cat - 1], i)
                max_h[a[i][j].cat - 1] = max(max_h[a[i][j].cat - 1], i)
                min_w[a[i][j].cat - 1] = min(min_w[a[i][j].cat - 1], j)
                max_w[a[i][j].cat - 1] = max(max_w[a[i][j].cat - 1], j)
                cnt[a[i][j].cat - 1] += 1

    score = 0
    for i in range(n_cat):
        if cnt[i] > 0:
            if cnt[i] != (max_h[i] - min_h[i] + 1) * (max_w[i] - min_w[i] + 1):
                return -1
            score += d0 * (cnt[i] / (w * h))**0.5
    return score


def calculate_brand_score(a: List[List[Item]], h: int, w: int) -> float:
    score_matrix = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(a[i][j].c)
        score_matrix.append(row)

    for i in range(h):
        state = []
        for j in range(i, h):
            left = 0
            for k in range(w + 1):
                if k != w:
                    if i == j:
                        state.append(a[i][k].brand)
                    else:
                        if state[k] != a[j][k].brand:
                            state[k] = -1
                if k > 0:
                    if state[k - 1] != -1 and (k == w or state[k] != state[k - 1]):
                        a_score = 1 + math.log((j - i + 1) * (k - left), 2)
                        for u in range(i, j + 1):
                            for q in range(left, k):
                                score_matrix[u][q] = max(score_matrix[u][q], a[u][q].c * a_score)
                    if k != w:
                        if state[k] == -1 or state[k] != state[k - 1]:
                            left = k

    score = 0
    for i in range(h):
        for j in range(w):
            score += score_matrix[i][j]
    return score
