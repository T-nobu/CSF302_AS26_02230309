"""
Lab 1 - Question 1: Linear Search
Student Number: 02230309
"""


def linear_search_309(arr, target):
    """
    Performs a linear search for `target` in `arr`.
    Returns the index of `target` if found, else -1.
    Time Complexity: O(n)
    """
    for index_309 in range(len(arr)):
        if arr[index_309] == target:
            return index_309
    return -1


if __name__ == "__main__":
    sample_309 = [4, 2, 7, 1, 9, 5]
    print("Sample array:", sample_309)
    print("Index of 9:", linear_search_309(sample_309, 9))
    print("Index of 100:", linear_search_309(sample_309, 100))
