# Sorting and Inversions Lab

---

## Q1: Quicksort Variants

Comparisons and time for four variants on random, sorted, reverse-sorted and duplicate-heavy input (n = 1,000 to 16,000).

![Q1 output](![alt text](image.png))

**Summary:** Lomuto degrades to Θ(n²) on sorted, reverse and duplicate input. Hoare (first-element pivot) degrades on sorted and reverse input. Randomised quicksort degrades only on duplicates. Three-way degrades on sorted and reverse input but is the best on duplicates.

---

## Q2: Counting Sort and Radix Sort

### Stability check

![Q2 stability](![alt text](image-1.png))

### Experiment A: n = 100,000, varying k

![Q2 output A](![alt text](image-2.png))

![Counting sort vs k](![alt text](image-4.png))

### Experiment B: k = 10^9, varying n

![Q2 output B](![alt text](image-3.png))

![Radix sort vs n](![alt text](image-5.png))

**Summary:** Counting sort is fast when k is small but loses once k is much larger than n. Radix sort grows linearly in n and wins over merge sort for large n, with base 256 faster than base 10.

---

## Q3: Counting Inversions

### Verification and timing

![Q3 timing](![alt text](image-6.png))

### Kendall tau for two users' movie rankings

![Q3 Kendall tau](![alt text](image-7.png))

**Summary:** Brute force is O(n²) and becomes impractical early. The merge-sort version is O(n log n) and handles 1,000,000 elements.