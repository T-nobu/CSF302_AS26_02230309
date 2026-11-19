# Closest Pair of Camera Traps (CSF302 Assignment 2)

Finds the two closest camera traps in a list of `(x, y)` points, two ways:

- `closest_pair_brute(points)`: checks every pair, Θ(n²)
- `closest_pair(points)`: divide and conquer, Θ(n log n)

Both return `(d, i, j)`: the smallest distance and the indices `i < j`.

## Files

| File | Purpose |
|---|---|
| `closest.py` | Both implementations (Part A) |
| `test_closest.py` | 12 tests (Part B) |
| `benchmark.py`, `bench2.py` | Timing runs (Part C) |
| `plot.py` | Draws the graph |

## Run

```bash
pip install pytest matplotlib
python -m pytest -v test_closest.py
python benchmark.py
```

## Tests: all passing

![Tests](![alt text](image.png))

## Analysis

Recurrence: `T(n) = 2T(n/2) + Θ(n)`. By the Master Method (a = 2, b = 2, f(n) = Θ(n) = Θ(n^log₂2), Case 2): **T(n) = Θ(n log n)**.

### Timing

![Timing table](![alt text](image-1.png))

![Log-log graph](![alt text](image-2.png))

Brute force quadruples when n doubles (Θ(n²)). Divide and conquer grows a little faster than 2× per doubling (n log n).

### Crossover

Divide and conquer becomes faster at **n = 36** on my machine.

![Crossover](![alt text](image-3.png))