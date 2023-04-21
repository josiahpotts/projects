# Name: Josiah Potts
# Modified: 8/1/2022
# Description: Uses the Dynamic Array data structure to use operations of a minimum heap.


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Method: add()
        Parameters: node: object
        Returns: node: object
        Description: Appends the desired object to the end of the dynamic array using upward percolation to put it
                    in the correct position of a heap tree.
        """
        #Call the dynamic array's method of append()
        self._heap.append(node)
        #Initialize a variable that will be used for storing current index of node through percolation. Initialize variable for while loop.
        node_index = self._heap.length() - 1
        check = True

        #If there is only one element in the heap then no need to percolate.
        if self._heap.length() > 1:
            #Percolate up the heap tree.
            while check == True:
                #Index of parent to the inserted node.
                node_parent = int(((node_index) - 1) / 2)
                #If value inserted is less than it's parent, switch spots.
                if node < self._heap[node_parent]:
                    temp = self._heap[node_parent]
                    self._heap[node_parent] = node
                    self._heap[node_index] = temp
                    node_index = node_parent
                #Change loop condition if percolation is complete.
                else:
                    check = False

    def is_empty(self) -> bool:
        """
        Method: is_empty()
        Parameters: None
        Returns: bool
        Description: Calls the is_empty() method from the dynamic array and returns true or false.
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        Method: get_min()
        Parameters: None
        Returns: object
        Description: If heap is empty raise exception. Otherwise, return the root of the tree which will be the minimum value.
        """
        #Check if heap is empty.
        if self._heap.is_empty() == True:
            raise MinHeapException
        #Return index zero as it is the root of the heap tree.
        else:
            return self._heap[0]

    def remove_min(self) -> object:
        """
        Method: remove_min()
        Parameters: None
        Returns: object
        Description: Removes the root value of the heap tree and uses _percolate_down() function to restructure heap
                    appropriately.
        """
        #Check if heap is empty.
        if self._heap.is_empty() == True:
            raise MinHeapException

        #Save the removed value for returning.
        removed = self._heap[0]
        #Replace root value with last heap value.
        self._heap[0] = self._heap[self._heap.length() - 1]
        #Remove last heap value to adjust heap size.
        self._heap.remove_at_index(self._heap.length() - 1)
        #Initialize where the parent index is at zero for percolation and initialize check variable for while loop.
        parent_index = 0
        check = True

        #Iterate through heap using _percolate_down() function until no more percolation needed.
        while check == True:
            #Pass to _percolate_down() the dynamic array and index of the parent we are percolating.
            child_swap = _percolate_down(self._heap, parent_index)
            #_percolate_down() will return the index of where the parent node is now, if changed it will need another percolate check, if not, break the loop.
            if child_swap == parent_index:
                check = False
            #Update where the parent node is for next iteration.
            else:
                parent_index = child_swap

        #Return the removed value.
        return removed



    def build_heap(self, da: DynamicArray) -> None:
        """
        Method: build_heap()
        Parameters: da: DynamicArray
        Returns: None
        Description: Takes a dynamic array and creates a valid heap from it.
        """
        #Clear heap of any existing values.
        self.clear()

        #Populate heap with dynamic array values.
        for x in range(da.length()):
            self._heap.append(da[x])

        #Initialize first non-leaf index to be check for valid heap.
        non_leaf_index = int(((self._heap.length()) / 2 ) - 1)
        #Initialize different variable for iteration length adding one for zero index.
        iteration_length = non_leaf_index + 1

        #Iterate through starting parent leaf to root.
        for x in range(iteration_length):
            #Initialize local check variable and copy the working index to a new variable for alteration.
            check = True
            index = non_leaf_index
            #Percolate the node downwards for height of the heap.
            while check == True:
                swap = _percolate_down(self._heap, index)
                if swap == index:
                    check = False
                else:
                    index = swap
            #Decrease parent node by one for next iteration.
            non_leaf_index -= 1


    def size(self) -> int:
        """
        Method: size()
        Parameters: None
        Returns: int
        Description: Returns the length of the dynamic array which is the size.
        """
        #Utilize length() method from the dynamic array.
        return self._heap.length()

    def clear(self) -> None:
        """
        Method: clear()
        Parameters: None
        Returns: None
        Description: Clears the current heap to empty.
        """
        #Assign a new, empty heap to the variable where there once was data.
        self._heap = DynamicArray()


def arrange_into_heap(da: DynamicArray) -> None:

    for x in range(da.length()):
        da.append(da[x])

    # Initialize first non-leaf index to be check for valid heap.
    non_leaf_index = int(((da.length()) / 2) - 1)
    # Initialize different variable for iteration length adding one for zero index.
    iteration_length = non_leaf_index + 1

    # Iterate through starting parent leaf to root.
    for x in range(iteration_length):
        # Initialize local check variable and copy the working index to a new variable for alteration.
        check = True
        index = non_leaf_index
        # Percolate the node downwards for height of the heap.
        while check == True:
            swap = _percolate_down(da, index)
            if swap == index:
                check = False
            else:
                index = swap
        # Decrease parent node by one for next iteration.
        non_leaf_index -= 1

    for x in range(int(da.length() / 2), da.length() - 1):
        da.remove_at_index(int(da.length() / 2 + 1))

def heapsort(da: DynamicArray) -> None:
    """
        Method: heapsort()
        Parameters:
        Returns:
        Description:
    """
    arrange_into_heap(da)
###################################################################################################
#I DON'T KNOW HOW TO DO THIS WITHOUT CREATING ANY SORT OF NEW DATA STRUCTURE OR USING RECURSION(!)#
###################################################################################################

# It's highly recommended that you implement the following optional          #
# function for percolating elements down the MinHeap. You can call           #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int) -> object:
    """
        Function: _percolate_down()
        Parameters: da: DynamicArray, parent: int
        Returns: object
        Description: Handles one instance of downward percolation. Checks special cases such as one child, two children,
                    and same values in children. Sets the lesser value to the minimum child and swaps for percolation.
    """
    #Initialize left child variable at None.
    left_child = None
    #Finds left child index and if index is valid it well set the left child index using heap's formula.
    if (2 * parent) + 1 < da.length():
        left_child = (2 * parent) + 1

    #Initialize right child variable at None.
    right_child = None
    #Finds right child index and if index is valid it will set the right child index using heap's formula.
    if (2 * parent) + 2 < da.length():
        right_child = (2 * parent) + 2

    #Initialize min_child variable for later use.
    min_child = None
#    print("left")
#    print(left_child)
#    print("right")
#    print(right_child)
#    print("parent value")
#    print(da[parent])
    #First check if there are no children to parent, adn if so then return.
    if left_child == None and right_child == None:
        return parent
    #Second check if left child only.
    elif left_child != None and right_child == None:
        min_child = left_child
    #Third check if right child only.
    elif right_child != None and left_child == None:
        min_child = right_child
    #Fourth check if left child and right child values equal each other and if so then set min_child to left child.
    elif da[left_child] == da[right_child]:
        min_child = left_child
    #Fifth check for both children if left child value is the smallest.
    elif da[left_child] < da[right_child]:
        min_child = left_child
    #Sixth check for both children if right child value is the smallest.
    elif da[right_child] < da[left_child]:
        min_child = right_child

    #Check if parent child is larger than its children's smallest value, if so then do a swap.
    if da[parent] > da[min_child]:
        temp = da[min_child]
        da[min_child] = da[parent]
        da[parent] = temp
    #If parent value is larger, return parent index.
    else:
        return parent

    #Return child index.
    return min_child

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
