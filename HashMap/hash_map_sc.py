# Name: Josiah Potts
# Due Date: 8/9/2022
# Description: This program is the HashMap data structure using singly linked list chaining methods.


from hash_include import (DynamicArray, LinkedList,
                          hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method: put()
        Parameters: key: str, value: object
        Returns: None
        Description: Puts key through hash function to generate the index and puts it in the Linked List at that index.
                    If the key already exists there it will be replaced with the new value instead of being created.
        """
        #Initialize the result of the key being put into the hash function.
        key_hash = self._hash_function(key)
        #Size the index to fit inside the current hash array.
        index = key_hash % self._buckets.length()

        #Check if there is a Linked List node with the same key.
        if self._buckets[index].contains(key) != None:
            #Replace the value in that node with new value.
            node = self._buckets[index].contains(key)
            node.value = value
        #Create new node at the index using insert() method, increment hashmap size by 1.
        else:
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Method: empty_buckets()
        Parameters: None
        Returns: int
        Description: Iterate the length of the bucket array to find empty Linked List which indicate empty buckets
                    and return the amount of empty buckets.
        """
        #Initialize empty variable with zero integer to start.
        empty = 0

        #Iterate the length of the buckets array.
        for _ in range(self._buckets.length()):
            #If length of the Linked List is zero then it is an empty bucket, increment empty by one.
            if self._buckets[_].length() == 0:
                empty += 1

        #Return the amount of empty buckets.
        return empty

    def table_load(self) -> float:
        """
        Method: table_load()
        Parameters: None
        Returns: float
        Description: Calculates the load of the hashmap.
        """
        #l = n / m
        load = self._size / self._capacity

        #Return calculation.
        return load

    def clear(self) -> None:
        """
        Method: clear()
        Parameters: None
        Returns: None
        Description: Resets HashMap by re-initializing itself with same capacity and hash function, and resets size to zero.
        """
        #Re-init self to reinitialize class variables, carrying over the same capacity, hash function.
        self.__init__(self._capacity, self._hash_function)
        #Reduce size to zero as the contents are cleared.
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method: resize_table()
        Parameters: new_capacity: int
        Returns: None
        Description: Creates a new hash table with prime capacity and rehashes prior values into the new hashmap.
        """
        #Does nothing if capacity change is less than one.
        if new_capacity < 1:
            return

        #If passed capacity is not a prime number, find the next prime number.
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)

        #Obtain key and value elements for later rehashing.
        keys_and_values = self.get_keys_and_values()

#        old_bucket = self._buckets
#        old_size = self._size
#        self._size = 0
#        self._capacity = new_capacity

#        for y in range(self._capacity):
#            self._buckets.append(LinkedList)

        #Reinitialize the hash to create a new hashmap with empty values but new capacity.
        self.__init__(new_capacity, self._hash_function)

#        for bucket in range(self._size):
#            if old_bucket[bucket].length() != 0:
#                for node in old_bucket[bucket]:
#                    self.put(node.value, node.value)
        if new_capacity == 2:
            self._capacity -= 1
            self._buckets.pop()

        #Use put() method to fill the hashmap with the same keys and values as before, but rehashed.
        for x in range(keys_and_values.length()):
            self.put(keys_and_values[x][0], keys_and_values[x][1])

    def get(self, key: str) -> object:
        """
        Method: get()
        Parameters: key: str
        Returns: object
        Description: Gets the node value in the hash map from the desired key.
        """
        #Rehash the key to end up at the same index.
        key_hash = self._hash_function(key)
        index = key_hash % self._buckets.length()

        #The index will be a bucket of linked lists, use contains() method in Linked Lists to find node.
        node = self._buckets[index].contains(key)

        #If key did not exist in the LL then it would be None, but if it does then return the value of that node.
        if node != None:
            return node.value
        else:
            return node

    def contains_key(self, key: str) -> bool:
        """
        Method: contains_key()
        Parameters: key: str
        Returns: bool
        Description: Utilize hashing to see if passed key exists in the hashmap.
        """
        #Rehash the passed key to end up where the key would be.
        key_hash = self._hash_function(key)
        index = key_hash % self._buckets.length()

        #Bucket will contain Linked List, use contains() method to find key in one of the nodes.
        if self._buckets[index].contains(key) == None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Method: remove()
        Parameters: key: str
        Returns: None
        Description: Removes a node in a linked list in the hashmap based on the key.
        """
        #Rehash the key to find index where key is at.
        key_hash = self._hash_function(key)
        index = key_hash % self._buckets.length()

        #Index will contain bucket of Linked List, use contain() to find the node with that key.
        if self._buckets[index].contains(key) != None:
            #If key is found then use Linked List method remove() to remove key and reset any addresses.
            self._buckets[index].remove(key)
            #Reduce size of hashmap by 1.
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method: get_keys_and_values()
        Parameters: None
        Returns: DynamicArray
        Description: Iterate all linked lists and nodes and store the keys and values into a DA.
        """
        #Initialize new empty DA.
        k_v = DynamicArray()

        #First iteration is through the length of the buckets dynamic array.
        for bucket in range(self._buckets.length()):
            #Check if there is a linked list node populated there.
            if self._buckets[bucket].length() != 0:
                #Second iteration is through the linked list, adding keys and values to a tuple and adding tuple to DA.
                for node in self._buckets[bucket]:
                    key_value_pair = (node.key, node.value)
                    k_v.append(key_value_pair)

        #Return the DA of keys and values.
        return k_v


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
        Method:
        Parameters:
        Returns:
        Description:
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mode_count = 1
    k_v = map.get_keys_and_values()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
