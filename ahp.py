import numpy as np


def get_weights(m):
    # https://giswin.geo.tsukuba.ac.jp/sis/gis_seminar/How%20to%20do%20AHP%20analysis%20in%20Excel.pdf
    for iy, ix in np.ndindex(m.shape):
        # changing lower diagonal only
        if ix >= iy:
            continue
        # populate with reciprocals from upper diagonal
        m[iy, ix] = 1 / m[ix, iy]
    n = np.zeros_like(m)
    for iy, ix in np.ndindex(n.shape):
        # divide by column-wise sum
        n[iy, ix] = m[iy, ix] / sum(m[:, ix])
    return np.sum(n, axis=1) / len(n)


def check_consistency(m, w):
    cm = [np.matmul(r, w) / w[i] for i, r in enumerate(m)]
    ci = ((sum(cm) / len(cm)) - len(cm)) / (len(cm) - 1)
    # TODO: generate ri dynamically to account for different grains of input matrices (e.g. 9-0-9 vs 5-0-5)
    ri = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.46, 1.49][len(cm)]
    return ci / ri


def utility(categories: dict[str, list[str]], weights: dict[str, float], candidate):
    total = 0
    for c, cr in categories.items():
        sub = 0
        for x in cr:
            sub += (candidate[x] * weights[x] if x in weights else 0)
        total += sub * weights[c]
    return total