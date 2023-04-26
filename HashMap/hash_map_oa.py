# Name: Josiah Potts
# Due Date: 8/9/2022
# Description: This program operates the HashMap data structure open address methods.


from hash_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Description: Use hashing to find index in hashmap with the key to place both key and value into the index.
                    If collision occurs, use open addressing and quadratic probing to find open index.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair

        #Find hash and index from key.
        key_hash = self._hash_function(key)
        index = key_hash % self._buckets.length()
        #Initialize checking variable and counter for quadratic probing.
        quad_hash = False
        i = 1

        #While loop for quadradic probing.
        while quad_hash == False:
            #Check table load and resize if necessary.
            while self.table_load() > 0.5:
                self.resize_table(self._capacity * 2)
            #Check if index is empty or if it is occupied is it a removed value.
            if self._buckets[index] == None or self._buckets[index].is_tombstone == True:
                self._buckets[index] = HashEntry(key, value)
                #By putting values here it increases size of hashmap by 1.
                self._size += 1
                quad_hash = True
            #If key exists the value will be replaced.
            elif self._buckets[index].key == key:
                self._buckets[index].value = value
                quad_hash = True
            #If space totally unavailable for putting, quadratic probe.
            else:
                index = (key_hash + i * i) % self._buckets.length()
                i += 1

    def table_load(self) -> float:
        """
        Method: table_load()
        Parameters: None
        Returns: float
        Description: Return the load which is n / m (size / capacity).
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method: empty_buckets
        Parameters: None
        Returns: int
        Description: Return the amount of empty buckets which is capacity minus the size.
        """
        return self._capacity - self._size

    def set_bucket_index(self, index: int, hash_entry: HashEntry) -> None:
        """
        Method: set_bucket_index()
        Parameters: index: int, hash_entry: HashEntry
        Returns: None
        Description: Sets the object at the desired index to the desired new object.
        """
        #Indexes below 0 are invalid.
        if index < 0:
            return
        #Set the bucket at the index to the new object.
        self._buckets[index] = hash_entry

    def get_buckets(self) -> object:
        """
        Method: get_buckets()
        Parameters: None
        Returns: object
        Description: Returns the DA of buckets from the HashMap.
        """
        return self._buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Method: resize_table()
        Parameters: new_capacity: int
        Returns: None
        Description: Adjusts passed capacity to a prime number, then adjusts HashMap's capacity to the new capacity.
                    This will create a temporary hashmap with temporary bucket values for setting the original buckets
                    to the new size.
        """

        #If new capacity is less than the size, this method does nothing.
        if new_capacity < self._size:
            return

        #If new capacity is not a prime number, find next prime number for capacity.
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)

        #Store current buckets into a new variable and create a new HashMap with new capacity.
        old_buckets = self._buckets
        temp = HashMap(new_capacity, self._hash_function)

        #Iterate through the old bucket for each object present.
        for bucket in range(old_buckets.length()):
            if old_buckets[bucket] != None and old_buckets[bucket].is_tombstone == False:
                #Utilize put() method to populate temporary HashMap with the same objects.
                temp.put(old_buckets[bucket].key, old_buckets[bucket].value)

        #Adjust capacity of original hashmap.
        self._capacity = new_capacity
        #Set original buckets to the temporary bucket with new capacity.
        self._buckets = temp.get_buckets()

    def get(self, key: str) -> object:
        """
        Method: get()
        Parameters: key: str
        Returns: object
        Description: Iterate through the bucket to find if the key exists and then return value if it does.
        """
        #Iterate through indexes of the bucket array.
        for bucket in range(self._buckets.length()):
            #Skip if bucket is empty.
            if self._buckets[bucket] != None:
                #Compare keys.
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                    #Return value of matching key.
                    return self._buckets[bucket].value

        #Key not found, return None.
        return None

    def contains_key(self, key: str) -> bool:
        """
        Method: contains_key()
        Parameters: key: str'
        Returns: bool
        Description: Iterate through the hashmap's buckets and compare keys. If key is found return True.
        """
        #Iterate through indexes of the bucket array.
        for bucket in range(self._buckets.length()):
            #Skip if bucket is empty.
            if self._buckets[bucket] != None:
                #Compare keys.
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                    #Return true, the buckets contain key.
                    return True

        #Return false, the buckets do not contain the key.
        return False

    def remove(self, key: str) -> None:
        """
        Method: remove()
        Parameters: key: str
        Returns: None
        Description: Iterate through hashmap's buckets to find the desired key. If found set key and value of object
                    to None and set the is_tombstone variable to True.
        """
        #Iterate through indexes of the bucket array.
        for bucket in range(self._buckets.length()):
            #Skip if bucket is empty.
            if self._buckets[bucket] != None:
                #Compare keys.
                if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone == False:
                    #Remove key and value and set object to a tombstone. Remove one from size.
#                    self._buckets[bucket].key = None
#                    self._buckets[bucket].value = None
                    self._buckets[bucket].is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Method: clear()
        Parameters: None
        Returns: None
        Description: Clears HashMap, retaining capacity, resetting all buckets to None.
        """
        #Set buckets to new empty DA.
        self._buckets = DynamicArray()

        #Iterate length of capacity to set all indexes to None.
        for _ in range(self._capacity):
            self._buckets.append(None)

        #Set size of Hashmap to zero.
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method: get_keys_and_values()
        Parameters: None
        Returns: DynamicArray
        Description: Iterate through buckets and store key and value pairs in tuple at the index of new DA.
        """
        #Initialize new DA.
        k_v = DynamicArray()

        #Iterate through all indexes of the HashMap buckets.
        for bucket in range(self._buckets.length()):
            #If object exists and is not a tombstone, add them as a tuple to DA.
            if self._buckets[bucket] != None and self._buckets[bucket].is_tombstone == False:
                k_v.append((self._buckets[bucket].key, self._buckets[bucket].value))

        #Return the DA of keys and values.
        return k_v

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
