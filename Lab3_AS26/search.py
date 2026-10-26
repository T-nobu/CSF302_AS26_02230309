"""
search.py
Q3: Binary Search vs Ternary Search (Menu-Driven Program)

A menu-driven program that:
    1. Generates n sorted random numbers -> Array
    2. Displays the array
    3. Searches for a key using Binary Search
    4. Searches for a key using Ternary Search
    5. Reports step/frequency count for the BEST case (key found in
       minimum possible comparisons)
    6. Reports step/frequency count for the WORST case (key absent)
    7. Prints a step/frequency comparison table across increasing n

Both search functions return the number of comparisons made, so the
same instrumented functions are reused by every menu option.
"""

import random

# Global state for the current session's array.
current_array = []


# ---------------------------------------------------------------------------
# Instrumented search algorithms
# ---------------------------------------------------------------------------
def binary_search_counted(arr, key):
    """
    Standard binary search. One "comparison" is counted per iteration
    (one check of arr[mid] against key), matching the recurrence
    T(n) = T(n/2) + O(1).
    Returns (found: bool, index: int, comparisons: int).
    """
    comparisons = 0
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return True, mid, comparisons
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return False, -1, comparisons


def ternary_search_counted(arr, key):
    """
    Standard ternary search: splits the range into three parts using
    two probe points (mid1, mid2) per iteration, matching the
    recurrence T(n) = T(n/3) + O(1).

    Each iteration can make up to 3 comparisons (arr[mid1] == key,
    arr[mid2] == key, and one boundary comparison to decide which
    third to recurse into) -- counted individually below, which is
    important for the analysis in option 7: ternary search does MORE
    comparisons per level than binary search, even though it shrinks
    the search space by a factor of 3 instead of 2 each time.
    Returns (found: bool, index: int, comparisons: int).
    """
    comparisons = 0
    low, high = 0, len(arr) - 1

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        comparisons += 1
        if arr[mid1] == key:
            return True, mid1, comparisons

        comparisons += 1
        if arr[mid2] == key:
            return True, mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            high = mid1 - 1
        elif key > arr[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1

    return False, -1, comparisons


# ---------------------------------------------------------------------------
# Menu option implementations
# ---------------------------------------------------------------------------
def generate_array():
    global current_array
    try:
        n = int(input("Enter n (array size): "))
        low = int(input("Enter minimum value: "))
        high = int(input("Enter maximum value: "))
    except ValueError:
        print("Invalid input.")
        return
    values = [random.randint(low, high) for _ in range(n)]
    current_array = sorted(values)
    print(f"Generated a sorted array of {n} elements.")


def display_array():
    if not current_array:
        print("Array is empty. Use option 1 first.")
        return
    print(current_array)


def search_binary_menu():
    if not current_array:
        print("Array is empty. Use option 1 first.")
        return
    key = int(input("Enter key to search: "))
    found, index, comparisons = binary_search_counted(current_array, key)
    if found:
        print(f"Found at index {index}. Comparisons: {comparisons}")
    else:
        print(f"Not found. Comparisons: {comparisons}")


def search_ternary_menu():
    if not current_array:
        print("Array is empty. Use option 1 first.")
        return
    key = int(input("Enter key to search: "))
    found, index, comparisons = ternary_search_counted(current_array, key)
    if found:
        print(f"Found at index {index}. Comparisons: {comparisons}")
    else:
        print(f"Not found. Comparisons: {comparisons}")


def best_case_report():
    """
    Best case: the key is placed exactly where each algorithm's first
    probe lands, so it is found in the minimum possible number of
    comparisons (1 for binary, 1 for ternary).
    """
    if not current_array:
        print("Array is empty. Use option 1 first.")
        return
    n = len(current_array)

    bin_mid = (0 + n - 1) // 2
    bin_key = current_array[bin_mid]
    _, _, bin_comparisons = binary_search_counted(current_array, bin_key)

    ter_mid1 = 0 + (n - 1) // 3
    ter_key = current_array[ter_mid1]
    _, _, ter_comparisons = ternary_search_counted(current_array, ter_key)

    print("Best case (key found on first probe):")
    print(f"  Binary search  -> key = {bin_key}, comparisons = {bin_comparisons}")
    print(f"  Ternary search -> key = {ter_key}, comparisons = {ter_comparisons}")


def worst_case_report():
    """
    Worst case: the key is absent from the array, forcing the search
    to exhaust the full recursion depth before giving up.
    """
    if not current_array:
        print("Array is empty. Use option 1 first.")
        return

    absent_key = max(current_array) + 1  # guaranteed not present
    _, _, bin_comparisons = binary_search_counted(current_array, absent_key)
    _, _, ter_comparisons = ternary_search_counted(current_array, absent_key)

    print(f"Worst case (key = {absent_key}, guaranteed absent):")
    print(f"  Binary search  -> comparisons = {bin_comparisons}")
    print(f"  Ternary search -> comparisons = {ter_comparisons}")


def comparison_table():
    """
    Prints a step/frequency comparison table (worst case) for binary
    vs ternary search across increasing n, alongside the theoretical
    log2(n) and log3(n) bounds for reference.
    """
    import math

    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

    print(f"{'n':>10} | {'binary':>8} | {'log2(n)':>8} | "
          f"{'ternary':>8} | {'log3(n)':>8}")
    print("-" * 55)

    for n in sizes:
        arr = sorted(random.sample(range(n * 10), n))
        absent_key = max(arr) + 1

        _, _, bin_comparisons = binary_search_counted(arr, absent_key)
        _, _, ter_comparisons = ternary_search_counted(arr, absent_key)

        log2n = math.log2(n)
        log3n = math.log(n, 3)

        print(f"{n:>10} | {bin_comparisons:>8} | {log2n:>8.2f} | "
              f"{ter_comparisons:>8} | {log3n:>8.2f}")

    # -----------------------------------------------------------------
    # Conclusion:
    # Binary search halves the search space each step, giving the
    # recurrence T(n) = T(n/2) + O(1), which solves to O(log2 n)
    # comparisons in the worst case. Ternary search splits the space
    # into three parts, giving T(n) = T(n/3) + O(1), which solves to
    # O(log3 n) -- fewer *levels* of recursion, since log3(n) < log2(n)
    # for all n > 1.
    #
    # However, each ternary search level does up to 3 comparisons
    # (two probe checks plus a boundary check) instead of binary
    # search's 1 comparison per level. So the total worst-case
    # comparison count is approximately 3*log3(n) for ternary versus
    # 1*log2(n) for binary. Since log3(n) = log2(n) / log2(3) and
    # log2(3) ~= 1.585, ternary search's total is roughly
    # (3 / 1.585) * log2(n) ~= 1.89 * log2(n) -- meaning ternary search
    # typically makes MORE total comparisons than binary search, even
    # though it needs fewer recursive levels. This is why binary
    # search is generally preferred over ternary search in practice,
    # despite the smaller recurrence base.
    # -----------------------------------------------------------------


# ---------------------------------------------------------------------------
# Menu loop
# ---------------------------------------------------------------------------
def print_menu():
    print("\n----- Binary vs Ternary Search Menu -----")
    print("1. Generate n sorted random numbers -> Array")
    print("2. Display Array")
    print("3. Search for a key using Binary Search")
    print("4. Search for a key using Ternary Search")
    print("5. Step/frequency count for best case")
    print("6. Step/frequency count for worst case")
    print("7. Step/frequency count comparison table across increasing n")
    print("0. Exit")


def main():
    actions = {
        "1": generate_array,
        "2": display_array,
        "3": search_binary_menu,
        "4": search_ternary_menu,
        "5": best_case_report,
        "6": worst_case_report,
        "7": comparison_table,
    }

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Exiting.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
