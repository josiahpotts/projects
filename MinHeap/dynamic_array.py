# Name: Josiah Potts
# Modified: 7/11/2022
# Description: This program creates the Dynamic Array data structure. It includes functional methods that allow the user
#               to implement this Dynamic Array in all sorts of programs that require anything such as a list,
#               dictionary, and arrays as such. The Dynamic Array resized itself in order to grow during runtime,
#               causing it to differ from a Static Array.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Method: resize()
        Parameters: new_capacity: int
        Returns: None
        Description: The Dynamic Array adjusts its capacity to account for new data needing to be stored outside of current capacity.
        This method will create a new Dynamic Array with adjusted capacity and copy the contents of the smaller Dynamic Array to it.
        """
        #First check if new capacity is zero, as it cannot equal zero. Simply returns out of resizing.
        if new_capacity == 0:
            return

        #Secondly, check if capacity of Dynamic Array is less than size of stored data. If this is the case it simply returns out of resizing.
        if new_capacity < self._size:
            return

        #If neither unacceptable conditions weren't met, then the Dynamic Array adjusts its capacity to the new capacity.
        self._capacity = new_capacity

        #If there are contents in the array then they will need to be copied to the new Dynamic Array with adjusted capacity.
        copy = self._data
        self._data = StaticArray(self._capacity)

        #Check if there are contents in the array to copy.
        if self._size != 0:
            #Fills new Dynamic Array with the copied contents at appropriate index.
            for x in range(self._size):
                self._data[x] = copy[x]

    def append(self, value: object) -> None:
        """
        Method: append()
        Parameters: value: object
        Returns: None
        Description: Adds the passed value to the end of the array. If the capacity of the array is full then it will automatically
        call the resize() method to create a new Dynamic Array with adjusted capacity.
        """
        #Check if current Dynamic Array is full, if it is the capacity will be doubled.
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        #The size variable will always be the index at the end of the array and it adds the requested value to that index, then increases size by one.
        self._data[self._size] = value
        self._size = self._size + 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Method: insert_at_index()
        Parameters: index: int, value: object
        Returns: None
        Description: Inserts desired value at the index requested, shifting all other values to the right by one. If index passed
        is invalid (less than zero, or greater than size) it will raise a DynamicArrayException. If size is equal to capacity
        then the capacity will be doubled by calling the resize() method.
        """

        #Checks if index is valid for isnertion.
        if index < 0:
            raise DynamicArrayException
        elif index > self._size:
            raise DynamicArrayException

        #If size is equal to capacity then the capacity will double to allow room for insertion.
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        #Iterate through the existing Static Array, shifting each value to the next index until after the requested index, leaving that location with value None.
        for x in range(self._size - 1, index - 1, -1):
            self._data[x + 1] = self._data[x]

        #Set desired index from None to value passed to method, and increase the size tracking variable by one.
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Method: remove_at_index()
        Parameters: index: int
        Returns: None
        Description: Removes an element within the Dynamic Array, shifting all other elements and adjusting the size. Exceptions in place
        if the index request for removal is invalid.
        """
        #Check if array size is zero, index removal request is negative, and if the index is larger than the size of the array. Raises exceptions.
        if self._size == 0:
            raise DynamicArrayException
        elif index < 0:
            raise DynamicArrayException
        elif index > self._size - 1:
            raise DynamicArrayException

        #If size of data stored is more than 10 and less than 1/4 of the total capacity of the Dynamic Array, the capacity will be reduced to only twice the stored size.
        if self._capacity <= 10:
            self._capacity = self._capacity
        elif self._size < (self._capacity / 4):
            self.resize(self._size * 2)
            #If capacity falls below 10 from prior calculation, the capacity will be reset to 10.
            if self._capacity < 10:
                self._capacity = 10

        #If only 1 element, remove it. Else, loops through to shift all elements starting from the requested index.
        if index == self._size - 1:
            self._data[index] = None
        else:
            for x in range(index, self._size - 1):
                self._data[x] = self._data[x + 1]

        #Adjust size for removed element.
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Method: slice()
        Parameters: start_index: int, size: int
        Returns: DynamicArray()
        Description: Slices the elements from the desired element to the size of the slice. Checks are in place if slice size too big,
        or invalid. Creates a new Dynamic Array with the sliced elements in the same order and the desired size.
        """
        #Check if array size is zero, index removal request is negative, and if the index is larger than the size of the array. Raises exceptions.
        if self._size == 0:
            raise DynamicArrayException
        if start_index < 0:
            raise DynamicArrayException
        elif start_index > self._size - 1:
            raise DynamicArrayException
        elif size > (self._size - start_index):
            if size != 0:
                raise DynamicArrayException

        #Check if size is zero, return empty Dynamic Array. Check if size less than zero, return exception.
        if size == 0:
            empty_dyn = DynamicArray()
            return empty_dyn
        elif size < 0:
            raise DynamicArrayException

        #Create new Static Array with size of slice. Initialize counter variable for loop.
        new_static = StaticArray(size)
        counter = 0

        #Loop from starting index through the size of the slice, adding elements to the Static Array.
        for x in range(start_index, start_index + size):
            new_static[counter] = self._data[x]
            counter += 1

        #Create new Dynamic Array to return.
        new_dynamic = DynamicArray()

        #Loop through Static Array length, which is the same as the slice size, using append() method to fill in data.
        for x in range(new_static.length()):
            new_dynamic.append(new_static[x])

        #Return new Dynamic Array.
        return new_dynamic


    def merge(self, second_da: "DynamicArray") -> None:
        """
        Method: merge()
        Parameters: second_da: "DynamicArray"
        Returns: None
        Description: Takes the elements from a second Dynamic Array and appends it to the end of this Dynamic Array.
        Size and capacity get adjusted accordingly with append() and resize() methods.
        """
        #Loop through passed Dynamic Array to append each element.
        for x in range(second_da._size):
            self.append(second_da[x])

    def map(self, map_func) -> "DynamicArray":
        """
        Method: map()
        Parameters: map_func
        Returns: "DynamicArray"
        Description: Desired mapping function applied to each element of the Dynamic Array and the results are appended
        onto an new empty Dynamic Array which gets returned.
        """
        #Initialize empty Dynamic Array to fill with elements.
        new_dynamic = DynamicArray()

        #Loop through all elements of original Dynamic Array, applying the desired function map to the elements and appending them to new array.
        for x in range(self._size):
            new_dynamic.append(map_func(self._data[x]))

        #Return mapped Dynamic Array.
        return new_dynamic

    def filter(self, filter_func) -> "DynamicArray":
        """
        Method: filter()
        Parameters: filter_func
        Returns: "DynamicArray"
        Description: Checks every element in the Dynamic Array if it meets filtered conditions and returns and new
        Dynamic Array with the elements that do meet the condition.
        """
        #Initialize empty array to populate with filtered elements.
        new_dynamic = DynamicArray()

        #Loop through each element and test for the filter. If true, append element to filtered Dynamic Array.
        for x in range(self._size):
            if filter_func(self._data[x]) == True:
                new_dynamic.append(self._data[x])

        #Returns the filtered Dynamic Array.
        return new_dynamic

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Method: reduce()
        Parameters: reduce_func, initializer=None
        Returns: object
        Description: Applies the passed function to each element of the Dynamic Array, accumulating the result in new object variable.
        Considers if there is an initializer to start as the first item in the function and operates without the for loop if
        the Dynamic Array size only contains one element.
        """
        #Initialize the object the sum is going into if passed initializer is not None.
        if initializer != None:
            obj = initializer
        else:
            obj = self._data[0]

        #Loops through each element and applies them as "y" variable in passed function, adding to the "x" in the function which is the initialized object.
        for x in range(self._size - 1):
            if initializer != None and x == 0:
                obj = reduce_func(obj, self._data[x])
            if x != self._size - 1:
                obj = reduce_func(obj, self._data[x + 1])

        #If size is one element the loop above will not be entered, instead it will operate here.
        if self._size == 1 and initializer != None:
            obj = reduce_func(obj, self._data[0])

        #Returns the final object from reduction.
        return obj


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Funciton: find_mode
    Parameters: arr: Dynamic Array
    Returns: (DynamicArray, int)
    Description: Loops through the elements in a Dynamic Array to first find the size of the mode, then again for the elements
    that meet that size and add them to a Dynamic Array that contains all mode values.
    """
    #Initialize mode frequency as 1, counter starts at the frequency (1), and the Dynamic Array for mode values.
    frequency = 1
    counter = 1
    mode_da = DynamicArray()

    # Check each value after the first in Dynamic Array, counting frequency and setting it as the highest frequency.
    for x in range(1, arr.length()):
        if arr[x] == arr[x - 1]:
            counter += 1
            if counter > frequency:
                frequency = counter
        elif arr[x] != arr[x - 1]:
            counter = 1

    #Reset counter.
    counter = 1

    #Count each value and if the count of the value is equal to mode frequency then that value gets appended to the mode array.
    for y in range(1, arr.length()):
        #This conditions checks if the values all show up only once in the array.
        if frequency == 1 and y == 1:
            mode_da.append(arr[y - 1])
        if arr[y] == arr[y - 1]:
            counter += 1
        elif arr[y] != arr[y - 1]:
            counter = 1
        if counter == frequency:
            mode_da.append(arr[y])
            counter = 1

    #Special condition handling: if array only has 1 element it automatically is the mode.
    if arr.length() == 1:
        frequency = 1
        mode_da.append(arr[0])

    # Return tuple of mode Dynamic Array and amount of frequency.
    return (mode_da, frequency)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")


    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")

