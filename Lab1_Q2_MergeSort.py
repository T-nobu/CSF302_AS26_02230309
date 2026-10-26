"""
Lab 1 - Question 2: Merge Sort
Student Number: 02230309
"""


def merge_sort_309(arr):
    """
    Sorts `arr` in ascending order using merge sort.
    Returns a new sorted list (original is not modified).
    Time Complexity: O(n log n)
    """
    if len(arr) <= 1:
        return arr[:]

    mid_309 = len(arr) // 2
    left_309 = merge_sort_309(arr[:mid_309])
    right_309 = merge_sort_309(arr[mid_309:])

    return _merge_309(left_309, right_309)


def _merge_309(left_309, right_309):
    """Merges two sorted lists into one sorted list."""
    merged_309 = []
    i_309 = j_309 = 0

    while i_309 < len(left_309) and j_309 < len(right_309):
        if left_309[i_309] <= right_309[j_309]:
            merged_309.append(left_309[i_309])
            i_309 += 1
        else:
            merged_309.append(right_309[j_309])
            j_309 += 1

    merged_309.extend(left_309[i_309:])
    merged_309.extend(right_309[j_309:])
    return merged_309


if __name__ == "__main__":
    sample_309 = [5, 3, 8, 1, 9, 2]
    print("Unsorted:", sample_309)
    print("Sorted:", merge_sort_309(sample_309))
