"""
Lab 1 - Question 2: Bubble Sort
Student Number: 02230309
"""


def bubble_sort_309(arr):
    """
    Sorts `arr` in ascending order using bubble sort.
    Returns a new sorted list (original is not modified).
    Time Complexity: O(n^2)
    """
    result_309 = arr[:]
    n_309 = len(result_309)

    for i_309 in range(n_309):
        swapped_309 = False
        for j_309 in range(0, n_309 - i_309 - 1):
            if result_309[j_309] > result_309[j_309 + 1]:
                result_309[j_309], result_309[j_309 + 1] = result_309[j_309 + 1], result_309[j_309]
                swapped_309 = True
        if not swapped_309:
            break

    return result_309


if __name__ == "__main__":
    sample_309 = [5, 3, 8, 1, 9, 2]
    print("Unsorted:", sample_309)
    print("Sorted:", bubble_sort_309(sample_309))
