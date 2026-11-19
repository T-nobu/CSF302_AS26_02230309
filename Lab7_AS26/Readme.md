# Greedy, Graphs and Randomized Algorithms Lab 

---

## Q1: Activity Selection and Knapsack

![Q1 activity selection](![alt text](image.png))

![Q1 knapsack](![alt text](image-1.png))

**Explanation:** Earliest finish time is optimal for activity selection. Earliest start fails when one long early activity blocks the rest, and shortest duration fails when a short activity overlaps two others that fit together. Fractional knapsack is solved exactly by value/weight order (240), but the same rule on 0/1 knapsack gives only 160 against a DP optimum of 220. Over 100,000 random inputs the worst greedy/optimal ratio found was 0.077, and a constructed case shows it can be made arbitrarily bad.

---

## Q2: Huffman Coding

![Q2 code table](![alt text](image-2.png))

![Q2 compression](![alt text](image-3.png))

**Explanation:** Frequent characters get short codes and rare ones get long codes, so every file decoded back to the original. Compression depends on how skewed the frequencies are: DNA with 4 equally likely symbols needs exactly 2 bits each (25% of the original size), English text saves 46.4% and source code 41.1%. The ratios count only the encoded bits, not the cost of storing the code table.

---

## Q3: Shortest Paths and Minimum Spanning Trees

![Q3 Dijkstra](![alt text](image-4.png))

![Q3 MST and timing](![alt text](image-5.png))

![Q3 negative edge](![alt text](image-6.png))

**Explanation:** Kruskal and Prim agreed on all 300 random graphs. Kruskal was faster on both the sparse and the dense graph in this Python run (0.0011 s against 0.0018 s, and 0.060 s against 0.198 s). Kruskal's sort runs in C and it stops after V-1 edges are joined, while Prim pushes many entries onto a Python heap. In theory the two are close with a binary heap, and Prim's advantage on dense graphs only appears with an array-based O(V²) version. Dijkstra fails with a negative edge because it finalises a vertex before a cheaper route through the negative edge is found: it reports 2 for vertex 1 when the true distance is 1.

---

## Q4: Randomized Algorithms

![Q4 quickselect](![alt text](image-7.png))

![Q4 Miller-Rabin](![alt text](image-8.png))

![Q4 Carmichael](![alt text](image-9.png))

**Explanation:** Randomized quickselect runs in expected linear time and beat sorting at every size, by about 2.2 times at n = 1,000,000. Miller-Rabin and trial division agreed on every number. The 20 random numbers were all composite, where trial division stops early, so I also tested 5 primes: Miller-Rabin took 0.0006 s against 0.072 s for trial division. On the Carmichael number 561, one round answered "prime" in 15 of 1,000 runs (1.5%); the exact fraction of fooling bases is 8 out of 558 (1.4%), well under the theoretical 25% bound.