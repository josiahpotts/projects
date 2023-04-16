# Author: Josiah Potts
# Date: 1/17/2023
# Description: This program presents the enumeration and iteration algorithms solutions for the Maximum Subarray Problem.

import sys
import time

# Usage when run from the command line: python max_subarray_algs.py <filename>.
# Example usage:                        python max_subarray_algs.py num_array_500.txt

file_name = sys.argv[1]


f = open(file_name, "r")
A = [int(num) for num in f.readline().strip().split(" ")]
f.close()

def max_subarray_enumeration(A):
    """
    Computes the value of a maximum subarray of the input array by "enumeration."
    
    Parameters:
        A: A list (array) of n >= 1 integers.
    
    Returns:
        The sum of the elements in a maximum subarray of A.
    """

    max = 0

    for index in range(0, len(A) - 1):
        for sub_index in range(index, len(A) - 1):
            temp = 0
            for dub_sub_index in range(index, sub_index):
                temp += A[dub_sub_index]
            if temp > max:
                max = temp

    return max
    
def max_subarray_iteration(A):
    """
    Computes the value of a maximum subarray of the input array by "iteration."
    
    Parameters:
        A: A list (array) of n >= 1 integers.
    
    Returns:
        The sum of the elements in a maximum subarray of A.
    """

    max = 0

    for index in range(0, len(A) - 1):
        current_sum = 0
        for sub_index in range(index, len(A) - 1):
            current_sum += A[sub_index]
            if current_sum > max:
                max = current_sum

    return max

  
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

for alg in [max_subarray_enumeration, max_subarray_iteration]:
    print(file_name, time_alg(alg, A))

#my_test = [-10, 2, 7, -10, 12, 8, -4, -3, 8, 4]

#print(max_subarray_iteration(my_test))
#print(max_subarray_enumeration(my_test))