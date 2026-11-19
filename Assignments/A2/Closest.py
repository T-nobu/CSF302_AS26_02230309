import math


def _sq(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def closest_pair_brute(points):
    """Compare every pair. Theta(n^2)."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    best, bi, bj = _sq(points[0], points[1]), 0, 1
    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            d = _sq(pi, points[j])
            if d < best:
                best, bi, bj = d, i, j
    return math.sqrt(best), bi, bj


def closest_pair(points):
    """Divide and conquer. Theta(n log n)."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")

    # Sort indices by x once (O(n log n)); ties broken by y.
    idx = sorted(range(n), key=lambda k: (points[k][0], points[k][1]))

    def solve(lo, hi):
        """Solve idx[lo:hi]. Return (best_sq, i, j, indices sorted by y)."""
        size = hi - lo
        if size <= 3:  # base case: brute force on at most 3 points
            sub = idx[lo:hi]
            best, bi, bj = None, -1, -1
            for a in range(size):
                for b in range(a + 1, size):
                    d = _sq(points[sub[a]], points[sub[b]])
                    if best is None or d < best:
                        best, bi, bj = d, sub[a], sub[b]
            sub.sort(key=lambda k: points[k][1])
            return best, bi, bj, sub

        mid = (lo + hi) // 2
        mid_x = points[idx[mid]][0]          # dividing line
        lb, li, lj, ly = solve(lo, mid)
        rb, ri, rj, ry = solve(mid, hi)
        if lb <= rb:
            best, bi, bj = lb, li, lj
        else:
            best, bi, bj = rb, ri, rj

        # Merge the two y-sorted lists: O(n)
        merged = []
        a = b = 0
        while a < len(ly) and b < len(ry):
            if points[ly[a]][1] <= points[ry[b]][1]:
                merged.append(ly[a]); a += 1
            else:
                merged.append(ry[b]); b += 1
        merged.extend(ly[a:])
        merged.extend(ry[b:])

        # Strip of width 2*delta around the dividing line (squared compare)
        strip = [k for k in merged if (points[k][0] - mid_x) ** 2 < best]
        for a in range(len(strip)):
            pa = points[strip[a]]
            for b in range(a + 1, len(strip)):
                pb = points[strip[b]]
                dy = pb[1] - pa[1]
                if dy * dy >= best:          # at most ~7 neighbours pass this
                    break
                d = _sq(pa, pb)
                if d < best:
                    best, bi, bj = d, strip[a], strip[b]
        return best, bi, bj, merged

    best, i, j, _ = solve(0, n)
    if i > j:
        i, j = j, i
    return math.sqrt(best), i, j