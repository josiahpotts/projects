#Author: Josiah Potts
#Last Date Modified: 4/16/2023
#Description: This program runs the maximum suffix algorithm for the max subarray problem.

import sys
import time

# Usage when run from the command line: python max_subarray_algs.py <filename>.
# Example usage:                        python max_subarray_algs.py num_array_500.txt

file_name = sys.argv[1]

f = open(file_name, "r")
A = [int(num) for num in f.readline().strip().split(" ")]
f.close()

def max_subarray_recursion_inversion(A):
    """
    Computes the value of a maximum subarray of the input array by "recursion inversion" (i.e., dynamic programming).
    
    Parameters:
        A: A list (array) of n >= 1 integers.
    
    Returns:
        The sum of the elements in a maximum subarray of A.
    """
    #Current max will be set to first element in array, being the beginning "farthest right element"
    max_subarray = A[0]
    max_suffix = A[0]

    #Iterate through array after starting index, which is our current max.
    for x in range (1, len(A)):
        #Max suffix
        max_suffix = max(A[x], max_suffix + A[x])
        #Max suffix vs Max subarray
        max_subarray = max(max_subarray, max_suffix)

    return max_subarray

  
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

for alg in [max_subarray_recursion_inversion]:
    print(file_name, time_alg(alg, A))

