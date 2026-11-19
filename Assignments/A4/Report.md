# Assignment 4: Paro Community Hall Bookings

This report covers `booking.py` (Part A), `test_booking.py` (Part B), and the analysis (Parts C and D). The numbers in Part C come from `analysis.py`.

## Parts A and B: Implementation and Tests

`greedy_earliest_finish` and `greedy_highest_fee` sort the requests and accept each one that fits. `best_schedule` is the dynamic programming solution: it sorts by finish time, finds `p(j)` with a binary search, fills `OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))`, and walks back through the table to recover the chosen requests. `brute_force` tries every subset and is used only for checking. Each function returns `(total_fee, chosen)` with the indices in ascending order. The example from the assignment gives `(7500, [0, 3, 4])` for earliest finish and `(10000, [1, 4])` for `best_schedule`.

`test_booking.py` has 12 tests and all of them pass. They check `best_schedule` against `brute_force` on 600 random inputs of 0 to 10 requests, and check that every returned schedule is valid (no overlaps, correct total). The edge cases are no requests, one request, all overlapping, none overlapping, back-to-back requests (an event ending at 12 and one starting at 12 both fit), zero-length and identical requests, an unmodified input, and bad input. Another test checks that `greedy_earliest_finish` is optimal when all fees are equal, on 500 small random inputs and 200 inputs of 50 requests. As a check on the tests themselves, I changed the compatibility test from `>=` to `>` in a copy of the code and 3 of the 12 tests failed.

## Part C: Analysis

### C1. Counterexamples

For earliest finish, take `[(9, 12, 1000), (10, 16, 8000)]`. The first request ends earlier, so the rule accepts it and earns 1,000. The second request overlaps it and is rejected, but it pays 8,000, which is the optimum. The rule fails because it looks only at finish times and never at fees, so a cheap short event can block a valuable one.

For highest fee, take `[(9, 17, 10000), (9, 13, 6000), (13, 17, 6000)]`. The rule accepts the 10,000 request first, which fills the whole day and blocks the other two, so it earns 10,000. The other two requests fit back-to-back and earn 12,000 together. The rule fails because it looks only at the fee and ignores how much hall time a request uses, so one large fee can take up time that would earn more when split between several smaller events. Two requests are not enough for this rule: with two requests that overlap it takes the larger fee, which is optimal, and with two that do not overlap it takes both.

### C2. Why the Recurrence Is Correct

Sort the requests by finish time and look at the last request, request j, in the sorted order. An optimal schedule for requests 1 to j either leaves out request j or includes it. If it leaves j out, the schedule is an optimal schedule for requests 1 to j−1, which is `OPT(j−1)`. If it includes j, it cannot contain any request that overlaps j. Because the requests are sorted by finish time, the requests that do not overlap j are exactly the ones that finish no later than j starts, and these are requests 1 to p(j). The rest of the schedule must therefore be a valid schedule within requests 1 to p(j), and it must be an optimal one: if a better schedule existed there, swapping it in would still be valid, because every request in it ends before j starts, and it would raise the total, which contradicts the first schedule being optimal. So the best schedule that includes j earns `fee_j + OPT(p(j))`. The optimal answer is the larger of the two cases, which is the recurrence. This is optimal substructure: an optimal solution contains optimal solutions to smaller subproblems of the same form.

### C3. Greedy Revenue Compared with the Optimum

I generated 1,000 random inputs of 50 requests for each of two scenarios. In scenario A, start times are random from 0 to 200, durations from 1 to 30, and fees from 500 to 10,000 independent of length. In scenario B, the fee is roughly proportional to the duration (300 per time unit, multiplied by a random factor between 0.5 and 1.5). The ratio is greedy revenue divided by optimal revenue for each input; the average is the mean of those 1,000 ratios and the worst is the smallest.

| Scenario | Rule | Average ratio | Worst ratio | Inputs where optimal |
|---|---|---:|---:|---:|
| A: fee independent of length | Earliest finish | 0.826 | 0.542 | 0 of 1,000 |
| A: fee independent of length | Highest fee | 0.894 | 0.622 | 68 of 1,000 |
| B: fee proportional to length | Earliest finish | 0.545 | 0.233 | 0 of 1,000 |
| B: fee proportional to length | Highest fee | 0.939 | 0.762 | 92 of 1,000 |

Earliest finish was never optimal on inputs of this size. It does worst in scenario B because it favours short events, which are the ones that earn the least there. Highest fee does better in both scenarios but is still optimal in under 10% of the inputs.

### C4. Time Complexity

`greedy_earliest_finish` takes O(n log n): sorting costs O(n log n) and the scan is O(n). `greedy_highest_fee` takes O(n²) in the worst case: sorting is O(n log n), but each request is checked against every request already accepted, which can be up to n. `best_schedule` takes O(n log n): sorting is O(n log n), finding all the p(j) values with binary search is O(n log n), and filling the table and walking back are O(n). It uses O(n) extra space. `brute_force` takes O(n · 2ⁿ), because it looks at 2ⁿ subsets and checks each in O(n) time, which is why it is limited to n ≤ 15.

## Part D: Critical Reflection

**1. What does this say about testing as proof?** In my random tests on small inputs, earliest finish matched the optimum on 315 of 600 cases (52.5%) and highest fee on 534 of 600 (89.0%). A rule that is wrong in general can therefore pass most tests, and highest fee would have passed nearly nine checks out of ten. Finding the 3-request counterexample took reasoning about how the rule could fail, not more random testing. Tests can show that a rule is wrong, but passing tests cannot show that it is right. The dynamic programming solution also matched brute force on all 600 inputs, but my confidence in it comes from the proof of the recurrence, with the tests only as a check on my code.

**2. Should the manager keep the simple rule?** No. On 1,000 random inputs of 50 requests, earliest finish earned on average 82.6% of the optimal revenue when fees were independent of event length, and only 54.5% when fees were roughly proportional to length. Its worst cases were 54.2% and 23.3%, and it was never optimal in any of the 2,000 inputs. That loses between a sixth and nearly half of the revenue. The dynamic programming solution runs in O(n log n), the same as the sort the greedy rule needs, so the manager gains money and pays nothing extra. Highest fee did better (average 89.4% and 93.9%) but is still not guaranteed to be optimal, so it is not a safe replacement either.

**3. Why does greedy work with equal fees but fail otherwise?** With equal fees, maximising revenue means fitting in as many events as possible. Earliest finish leaves the most time for the remaining events, and if an optimal schedule starts with a different event, swapping in the earliest-finishing one cannot cause a clash, so the count never drops. With different fees, an event that finishes early may be worth very little and can block a much more valuable one, as in my first counterexample (1,000 against 8,000). The rule looks only at time, so that swap can lose money. This matches my tests: with equal fees, earliest finish was optimal on all 700 random inputs.

**4. Evaluating AI Claims on Greedy Optimality?**When asked how to maximize booking revenue, an AI tool initially suggested sorting requests by highest fee or highest fee-per-hour, framing them as fast, optimal greedy strategies. This claim confuses unweighted interval scheduling—where earliest-finish is provably optimal—with weighted interval scheduling, where no local greedy rule works. To verify the AI's claim, I implemented both greedy heuristics alongside an exhaustive brute_force solver and ran randomized differential testing (test_booking.py). Within milliseconds, small 3-request counterexamples like [(8, 16, 6000), (8, 12, 4000), (12, 16, 4000)] proved that the AI's greedy suggestions missed optimal combinations, confirming that dynamic programming is required for exact results.