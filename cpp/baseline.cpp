#define _CRT_SECURE_NO_WARNINGS 1 

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <map>
#include <set>
#include <cmath>

using namespace std;

#define MAXN 5000
#define MAXC 50
#define MAXB 50
#define MAXW 100
#define MAXH 10

typedef struct item{
	int ind;
	int cat;
	int brand;
	int c;
} item;

vector<item> items;
vector<item> cat2items[MAXC];

bool compare_items(const item &a, const item &b) {
	return a.c > b.c || a.c == b.c && a.brand < b.brand;
}

bool compare_items_by_brand(const item &a, const item &b) {
	return a.brand < b.brand || a.brand == b.brand && a.c > b.c;
}


typedef struct rectangle {
	int w;
	int h;
} rectangle;

double cat_score[MAXC + 1][MAXH + 1][MAXW + 1] = { 0 };
vector<item> cat_score_items[MAXC + 1][MAXH + 1][MAXW + 1];
double c[MAXC + 1][MAXW + 1] = { 0 };
rectangle c_best[MAXC + 1][MAXW + 1];

item sh[MAXH][MAXW];
double score_matrix[MAXH][MAXW] = { 0 };


double calculate_brand_score(item a[MAXH][MAXW], int h, int w) {
	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			score_matrix[i][j] = a[i][j].c;
		}
	}
	for (int i = 0; i < h; i++) {
		vector<int> state;
		for (int j = i; j < h; j++) {
			int left = 0;
				
			for (int k = 0; k <= w; k++) {
				if (k != w) {
					if (i == j) {
						state.push_back(a[i][k].brand);
					}
					else {
						if (state[k] != a[j][k].brand) {
							state[k] = -1;
						}
					}
				}
				if (k > 0) {
					if (state[k - 1] != -1 && (k == w || state[k] != state[k - 1])) {
						double a_score = (1 + log(1.0 * (j - i + 1) * (k - left)) / log(2));
						for (int u = i; u <= j; u++) {
							for (int q = left; q < k; q++) {
								score_matrix[u][q] = max(score_matrix[u][q], 1.0 * a[u][q].c * a_score);
							}
						}
					}
					if (k != w) {
						if (state[k] == -1 || state[k] != state[k - 1]) {
							left = k;
						}
					}
				}
			}
		}
	}
	double res = 0;
	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			res += score_matrix[i][j];
		}
	}
	return res;
}

double calculate_cat_score(item a[MAXH][MAXW], int h, int w, int n_cat, int d0) {
	vector<int> min_h, max_h, min_w, max_w, cnt;
	for (int i = 0; i < n_cat; i++) {
		min_h.push_back(h + 1);
		max_h.push_back(-1);
		min_w.push_back(w + 1);
		max_w.push_back(-1);
		cnt.push_back(0);
	}
	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			if (a[i][j].cat != -1) {
				min_h[a[i][j].cat - 1] = min(min_h[a[i][j].cat - 1], i);
				max_h[a[i][j].cat - 1] = max(max_h[a[i][j].cat - 1], i);
				min_w[a[i][j].cat - 1] = min(min_w[a[i][j].cat - 1], j);
				max_w[a[i][j].cat - 1] = max(max_w[a[i][j].cat - 1], j);
				cnt[a[i][j].cat - 1] += 1;
			}
		}
	}
	double score = 0;
	for (int i = 0; i < n_cat; i++) {
		if (cnt[i] > 0) {
			if (cnt[i] != (max_h[i] - min_h[i] + 1) * (max_w[i] - min_w[i] + 1)) {
				return -1;
			}
			score += 1.0 * d0 * sqrt(1.0 * (cnt[i]) / (w * h));
		}
	}
	return score;
}

double calculate_final_score(item a[MAXH][MAXW], int h, int w, int n_cat, int d0) {
	double cat_score = calculate_cat_score(a, h, w, n_cat, d0);
	if (cat_score == -1) {
		return -1;
	}
	double brand_score = calculate_brand_score(a, h, w);
	return cat_score + brand_score;
}


void run() {

	std::cout.precision(5);
	std::cout.setf(ios::fixed);

	int n, k, m, h, w, d0, ti, bi, ci;
	cin >> n >> k >> m >> h >> w >> d0;
	for (int i = 0; i < k; i++) {
		cat2items[i] = vector<item>();
	}
	for (int i = 0; i < n; i++) {
		cin >> ti >> bi >> ci;
		cat2items[ti - 1].push_back({ (i + 1), ti, bi, ci });
	}

	
	/*
	for each category sort items by cost in descending order(and secondary sort by brand for reproducibility)
	see compare_items function at the top of file
	*/
	for (int i = 0; i < k; i++) {
		sort(cat2items[i].begin(), cat2items[i].end(), compare_items);
	}

	/*
	calculate for each triple (cat - category, h - rectangle height, w - rectangle width):
		cat_score[cat][h][w] - estimate of score using greedy filling approach
		cat_score_items[cat][h][w] - ordered list of items for shelf filling
	*/
	for (int i = 0; i < k; i++) {
		for (int hh = 1; hh <= h; hh++) {
			for (int ww = 1; ww <= w; ww++) {
				double simple_brand_score = 0;
				int n_real = min((int)cat2items[i].size(), ww * hh);
				for (int j = 0; j < n_real; j++) {
					simple_brand_score += cat2items[i][j].c;
				}
				cat_score_items[i][hh][ww].clear();
				vector<item> tmp;
				for (int j = 0; j < n_real; j++) {
					tmp.push_back(cat2items[i][j]);
				}
				// group(sort) choosed items by brand (and secondary sort by cost for reproducibility)
				// (see compare_items_by_brand function at the top of file)
				sort(tmp.begin(), tmp.end(), compare_items_by_brand);
				for (int j = 0; j < n_real; j++) {
					cat_score_items[i][hh][ww].push_back(tmp[j]);
				}
				cat_score[i][hh][ww] = simple_brand_score + 1.0 * d0 * sqrt(1.0 * (n_real) / (w * h));
			}
		}
	}

	/*
	DP(Dynamic Programming) part to find optimal rectangle size for each category
		c[i][j] - best estimate of score for shelf size = (h x j) if we used only categories 1..i
		c_best[i][j] - for shelf size = (h x j) stores best rectangle(w_cat, h_cat) for i-th category
		(is necessary for fast answer recovering)
	*/
	for (int i = 0; i <= k; i++) {
		for (int j = 0; j <= w; j++) {
			c[i][j] = 0;
			c_best[i][j] = { 0, 0 };
		}
	}
	for (int i = 0; i < k; i++) {
		for (int j = 0; j <= w; j++) {
			int n_items_in_cat_i = cat2items[i].size();
			// brute force all possible rectangle sizes for i-th category
			for (int w_cat = 0; w_cat <= min(n_items_in_cat_i, w - j); w_cat++) {
				for (int h_cat = 0; h_cat * w_cat <= n_items_in_cat_i && h_cat <= h; h_cat++) {
					double new_score = c[i][j] + cat_score[i][h_cat][w_cat];
					if (c[i + 1][j + w_cat] < new_score) {
						c[i + 1][j + w_cat] = new_score;
						c_best[i + 1][j + w_cat] = { w_cat, h_cat };
					}
				}
			}
		}
	}

	/*
	Answer recovering part using c_best matrix
	*/
	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			sh[i][j] = { 0, -1, -1, 0 };
		}
	}
	int i = k;
	int j = w;
	while (i > 0) {
		rectangle ij_best = c_best[i][j];
		int cc = 0;
		for (int u = 0; u < ij_best.h; u++) {
			for (int q = j - ij_best.w; q < j; q++) {
				sh[u][q] = cat_score_items[i - 1][ij_best.h][ij_best.w][cc];
				cc += 1;
			}
		}
		i -= 1;
		j -= ij_best.w;
	}

	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			std::cout << sh[i][j].ind << " ";
		}
		std::cout << endl;
	}
}

int main(int argc, char *argv[])
{
	run();
	return 0;
}
