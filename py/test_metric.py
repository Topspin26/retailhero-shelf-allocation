from base import Item, create_empty_matrix
from metric import calculate_brand_score, calculate_cat_score, calculate_final_score


def test_from_example():
    '''
        shelf from example
        .567
        .12.
        .438
        ...9
        
        cat    brand  c      A[i]
        .222   .113   .439   .441   
        .11.   .11.   .23.   .44.   
        .113   .322   .X56   .122   
        ...3   ...2   ...7   ...2
          
        *X means 10
    '''

    h = w = 4
    k = m = 3
    d0 = 50

    a = create_empty_matrix(h, w)
    a[0][1] = Item(5, 2, 1, 4)
    a[0][2] = Item(6, 2, 1, 3)
    a[0][3] = Item(7, 2, 3, 9)
    a[1][1] = Item(1, 1, 1, 2)
    a[1][2] = Item(2, 1, 1, 3)
    a[2][1] = Item(4, 1, 3, 10)
    a[2][2] = Item(3, 1, 2, 5)
    a[2][3] = Item(8, 3, 2, 6)
    a[3][3] = Item(9, 3, 2, 7)

    assert calculate_brand_score(a, h, w) == 91
    assert abs(calculate_cat_score(a, h, w, k, d0) - 64.328) < 1e-3
    assert abs(calculate_final_score(a, h, w, k, d0) - 155.328) < 1e-3


def test_incorrect_shelf():
    h = w = 2
    k = m = 2
    d0 = 50

    a = create_empty_matrix(h, w)
    a[0][0] = Item(1, 1, 1, 1)
    a[0][1] = Item(2, 2, 1, 1)
    a[1][0] = Item(3, 2, 2, 1)
    a[1][1] = Item(4, 1, 2, 1)

    assert calculate_cat_score(a, h, w, k, d0) == -1
    assert calculate_final_score(a, h, w, k, d0) == -1
