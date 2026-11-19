# Sorting Nightly Transactions (CSF302 Assignment 3)

Two in-place quicksorts for a list of integers:

- `quicksort_basic(a)`: Lomuto partition, last element as pivot
- `quicksort_improved(a, cutoff=16)`: random pivot, insertion sort for parts of size ≤ `cutoff`, recurse on the smaller part and loop on the larger (depth O(log n))
- `quicksort_improved_3way(a, cutoff=16)`: **extra**, not required. Same as improved but with a 3-way partition (explained under Duplicates).

## Files

| File | Purpose |
|---|---|
| `sorts.py` | The sorts (Part A) |
| `test_sorts.py` | 50 test cases (Part B) |
| `benchmark.py` | All timings (Part C) |
| `shots.py` | Builds the tables and graphs below |

## Run

```bash
pip install pytest matplotlib
python -m pytest -v test_sorts.py
python benchmark.py
```

## Tests: all passing

![Tests](![alt text](image.png))

## Timing (n = 1,000 … 64,000)

![Tables](![alt text](image-1.png))

![Graphs](![alt text](image-2.png))

- **Random:** both sorts grow as n log n and are about equal.
- **Sorted:** `quicksort_basic` crashes with `RecursionError` at every size. `quicksort_improved` is fine.
- **Duplicates (0–9):** `quicksort_basic` works up to n = 8,000, then crashes with `RecursionError`. `quicksort_improved` never crashes but slows down quadratically (about 10 s at n = 64,000). `quicksort_improved_3way` stays fast (about 12 ms).

## Why basic quicksort fails: T(n) = T(n − 1) + Θ(n)

On sorted input the last element is the maximum, so Lomuto splits n elements into n − 1 and 0. One partition costs Θ(n), so

T(n) = T(n − 1) + Θ(n) = n + (n − 1) + … + 1 = Θ(n²).

The recursion also goes n levels deep, and Python's default limit is about 1,000, hence `RecursionError`. Duplicates cause the same split: every part made only of equal values splits into m − 1 and 0.

To see the quadratic cost without the crash, I raised the recursion limit and timed `quicksort_basic` on sorted input. Time grows about 4× each time n doubles:

![Quadratic](![alt text](image-3.png))

## Best cutoff

n = 100,000 random values, best of 7. **Cutoff = 16 is fastest (92 ms).** Cutoffs 8 and 32 are within about 7% of it, so the exact choice among them is close to noise.

![Cutoff](![alt text](image-4.png))

## Comparison with `sorted()`

![vs sorted](![alt text](image-5.png))

`sorted()` is about 6.7× faster than my best version.

## Notes

- On random data `quicksort_improved` is **not** noticeably faster than `quicksort_basic` (92 ms vs 87 ms at n = 100,000). What it gains is safety on sorted and duplicate-heavy input.
- Timings are from one machine and vary a little between runs. Rerun `benchmark.py` on your own machine for your numbers.