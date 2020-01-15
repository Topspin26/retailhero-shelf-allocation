import os
import numpy as np
from itertools import product


def generate_one(seed, h=None, w=None, n=None, k=None, m=None, d0=None, n_cat_for_brand=None, a=None, b=None, ksi=None):
    np.random.seed(seed)

    if h is None:
        h = np.random.randint(1, 11)
    if w is None:
        w = np.random.randint(1, 101)

    if n is None:
        coef = 0.5 + np.random.randint(3)
        n = max(1, int(w * h * coef))

    if k is None:
        k = np.random.randint(1, 51)
    if m is None:
        m = np.random.randint(1, 51)

    if d0 is None:
        d0 = 10 ** (np.random.randint(1, 7))

    p = np.random.randint(1, 1001, k)
    p = p / np.sum(p)
    q = np.random.randint(1, 1001, m)
    q = q / np.sum(q)

    if a is None:
        a = np.random.randint(1, 501, k)
    else:
        a = [a] * k
    if b is None:
        b = np.random.randint(1, 501, m)
    else:
        b = [b] * m

    brand_cat = set()
    for i in range(m):
        n_cat_for_brand_i = n_cat_for_brand
        if n_cat_for_brand_i is None:
            n_cat_for_brand_i = np.random.randint(1, 11)
        n_cat_for_brand_i = min(n_cat_for_brand_i, k)
        for j in np.random.choice(range(k), n_cat_for_brand_i, replace=False):
            brand_cat.add((i, j))

    items = []
    for i in range(n):
        cat, brand = np.random.choice(k), np.random.choice(m)
        while (brand, cat) not in brand_cat:
            cat, brand = np.random.choice(k), np.random.choice(m)
        ksi_i = ksi
        if ksi_i is None:
            ksi_i = 0.5 + np.random.random() / 2
        c = round(ksi_i * (a[cat] + b[brand]))
        items.append([cat + 1, brand + 1, int(c)])
    return n, k, m, h, w, d0, items


def generate_max_tests():
    params = dict(
        h=[1, 10],
        w=[1, 100],
        k=[1, 50],
        m=[1, 50],
        d0=[1, 1000000],
        n=[1, 5000],
        n_cat_for_brand=[1, 10],
        ab=[(1, 1), (500, 500), (None, None)],
        ksi=[1]
    )

    for i, vals in enumerate(product(*params.values())):
        p = dict(zip(params, vals))
        p['a'] = p['ab'][0]
        p['b'] = p['ab'][1]
        del p['ab']
        yield p


def save_random_tests(dirname, cnt=100):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for i in range(cnt):
        print(i)
        data = generate_one(i)
        save_test(data, os.path.join(dirname, str(i).zfill(3) + '.txt'))


def save_max_tests(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for i, p in enumerate(generate_max_tests()):
        print(i)
        data = generate_one(i, **p)
        save_test(data, os.path.join(dirname, str(i).zfill(3) + '.txt'))


def save_test(data, filename):
    n, k, m, h, w, d0, items = data
    with open(filename, 'w', encoding='utf-8') as fout:
        fout.write(f'{n} {k} {m} {h} {w} {d0}\n')
        for cat, brand, c in items:
            fout.write(f'{cat} {brand} {c}\n')


if __name__ == '__main__':
    save_random_tests(os.path.join('..', 'tests'))

    save_max_tests(os.path.join('..', 'max_tests'))
