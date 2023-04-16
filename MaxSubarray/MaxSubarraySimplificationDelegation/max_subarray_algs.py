# Author: Josiah Potts
# Date: 1/26/2023
# Description: This program presents the divide and conquer algorithm solutions for the Maximum Subarray Problem.

import sys
import time

# Usage when run from the command line: python max_subarray_algs.py <filename>.
# Example usage:                        python max_subarray_algs.py num_array_500.txt

file_name = sys.argv[1]

f = open(file_name, "r")
A = [int(num) for num in f.readline().strip().split(" ")]
f.close()

def find_max_crossing(A, low, mid, high):
    left_sum = 0
    sum = 0
    for i in range(mid, low, -1):
        sum = sum + A[i]
        if sum > left_sum:
            left_sum = sum

    right_sum = 0
    sum = 0
    for j in range(mid, high):
        sum = sum + A[j]
        if sum > right_sum:
            right_sum = sum

    return max(left_sum + right_sum - A[mid], left_sum, right_sum)

def max_subarray_simplification_delegation(A):
    """
    Computes the value of a maximum subarray of the input array by "simplification and delegation."
    
    Parameters:
        A: A list (array) of n >= 1 integers.
    
    Returns:
        The sum of the elements in a maximum subarray of A.
    """

    low = 0
    high = len(A) - 1
    mid = (low + high) // 2

    if low > high:
        return -1
    if low == high:
        return A[low]
    else:
        left = []
        for i in range(low, mid):
            left.append(A[i])
        left_sum = max_subarray_simplification_delegation(left)

        right = []
        for j in range(mid + 1, high):
            right.append(A[j])
        right_sum = max_subarray_simplification_delegation(right)

        cross_sum = find_max_crossing(A, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_sum
        else:
            return cross_sum

def time_alg(alg, A):
    """
    Runs an algorithm for the maximum subarray problem on a test array and times how long it takes.
    
    Parameters:
        alg: An algorithm for the maximum subarray problem.
        A: A list (array) of n >= 1 integers.
    
    Returns:
        A pair consisting of the value of alg(A) and the time needed to execute alg(A) in milliseconds.
    """

    start_time = time.monotonic_ns() // (10 ** 6) # The start time in milliseconds.
    max_subarray_val = alg(A)
    end_time   = time.monotonic_ns() // (10 ** 6) # The end time in milliseconds.
    return max_subarray_val, end_time - start_time

for alg in [max_subarray_simplification_delegation]:
    print(file_name, time_alg(alg, A))
