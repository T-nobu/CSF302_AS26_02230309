# Dynamic Programming Lab

---

## Q1: Rod Cutting

Maximum revenue and piece lengths for n = 1 to 10:

![Q1 revenue](![alt text](image.png))

Recursive calls and running time for n = 5 to 25:

![Q1 counts](![alt text](image-1.png))

**Explanation:** The naive version recomputes the same subproblems and makes 2^n calls (33,554,432 calls and about 7.5 s at n = 25). Memoization solves each subproblem once, so the call count grows only quadratically (326 calls at n = 25). Bottom-up does the same n(n+1)/2 inner steps with no recursion at all.

---

## Q2: Matrix Chain Multiplication

![Q2 output](![alt text](image-2.png))

**Explanation:** The DP gives 15,125 for the first test, as expected, and 158 for `<5, 4, 6, 2, 7>`. Every result matched the brute-force search. The left-to-right order costs much more in every case (for example 40,500 against 15,125 on the first test).

---

## Q3: Longest Common Subsequence

LCS table and reconstruction for `ABCBDAB` and `BDCABA`:

![Q3 table](![alt text](image-3.png))

DP versus brute force for string lengths 5 to 18:

![Q3 timing](![alt text](image-4.png))

Line-by-line diff of two text files:

![Q3 diff](![alt text](image-5.png))

**Explanation:** The DP takes O(mn) time, while trying every subsequence of X takes O(2^m · n). Brute force grows from under a millisecond to about 0.6 s at length 18 and doubles with each extra character, while the DP stays below 0.1 ms. The two-row version returns the same length using only O(n) memory, but it cannot reconstruct the subsequence.