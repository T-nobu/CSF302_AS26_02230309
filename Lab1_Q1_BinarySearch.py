"""
Lab 1 - Question 1: Binary Search
Student Number: 02230309
Note: Binary search requires the input array to be sorted first.
"""


def binary_search_309(arr, target):
    """
    Performs an iterative binary search for `target` in sorted `arr`.
    Returns the index of `target` if found, else -1.
    Time Complexity: O(log n)
    """
    low_309 = 0
    high_309 = len(arr) - 1

    while low_309 <= high_309:
        mid_309 = (low_309 + high_309) // 2
        if arr[mid_309] == target:
            return mid_309
        elif arr[mid_309] < target:
            low_309 = mid_309 + 1
        else:
            high_309 = mid_309 - 1
    return -1


if __name__ == "__main__":
    sample_309 = sorted([4, 2, 7, 1, 9, 5])
    print("Sorted sample array:", sample_309)
    print("Index of 9:", binary_search_309(sample_309, 9))
    print("Index of 100:", binary_search_309(sample_309, 100))
