#Author: Josiah Potts
#Date: 2/7/2023
#Description: Program uses the HuffmanCode class to create huffman codes.
            # To use, call helper function to get frequency and of some text file
            # and pass that result into the creation of a HuffmanCode class.
            # Then use methods encode and decode with strings to get results.
            # Cost calculations not implemented at this time...

import heapq # Hint: use Python's priority queue class, heapq.

class Node:
    def __init__(self, count, children):
        self.count    = count
        self.children = children
        
    def is_leaf(self):
        return False
        
    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count
        
class LeafNode(Node):
    def __init__(self, symbol, count):
        super().__init__(count, [])
        self.symbol = symbol
        
    def is_leaf(self):
        return True

class HuffmanCode:
    def __init__(self, F):
        self.C = dict()
        self.T = None
        self.cost = 0
        self.average_cost = 0

        #Create priority queue and initialize all nodes from frequency list
        heap = []
        for i in F:
            node = LeafNode(i, F[i])
            heapq.heappush(heap, node)

        heapq.heapify(heap)

        #Build the tree utilizing piority queue functionality
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            combined_freq = left.count + right.count
            node = Node(combined_freq, [left, right])
            heapq.heappush(heap, node)

        #Remaining node in priority queue is the root of the tree
        self.T = heapq.heappop(heap)

        #Use depth first search to create a path of the code
        self.dfs(self.T, "", self.C)

    def dfs(self, root, code_assignment, C):

        #Base case: it has reached a leaf of the tree
        if root.is_leaf() == True:
            C[root.symbol] = code_assignment
            return

        #If not a leaf of the tree, build the string code with the 0 for left nodes and 1 for right
        if root.children[0] is not None:
            self.dfs(root.children[0], code_assignment + '0', C)
        if root.children[1] is not None:
            self.dfs(root.children[1], code_assignment + '1', C)

    def encode(self, m):
        """
        Uses self.C to encode a binary message.
.    
        Parameters:
            m: A plaintext message.
        
        Returns:
            The binary encoding of the plaintext message obtained using self.C.
        """

        compressed_m = ""
        #Encode the message
        for i in m:
            for key in self.C:
                if key == i:
                    compressed_m += self.C[key]

        return compressed_m
        
    def decode(self, c):
        """
        Uses self.T to decode a binary message c = encode(m).
.    
        Parameters:
            c: A message encoded in binary using self.encode.
        
        Returns:
            The original plaintext message m decoded using self.T.
        """

        #Initialize message string and root node
        message = ""
        node = self.T

        #Loop until a leaf is hit, and add the symbol of the leaf to the message
        for i in c:
            if i == "1":
                node = node.children[1]
            if i == "0":
                node = node.children[0]
            if node.is_leaf() == True:
                    message += node.symbol
                    node = self.T

        return message

    def get_cost(self):
        """
        Returns the cost of the Huffman code as defined in CLRS Equation 16.4.
        
        Returns:
            Returns the cost of the Huffman code.
        """
        #TODO
                
        return self.cost
        
    def get_average_cost(self):
        """
        Returns the average cost of the Huffman code.
        
        Returns:
            Returns the average cost of the Huffman code.
        """
        #TODO
                
        return self.average_cost
        
def get_frequencies(s):
    """
    Computes a frequency table for the input string "s".
    
    Parameters:
        s: A string.
        
    Returns:
        A frequency table F such that F[c] = (# of occurrences of c in s).
    """

    F = dict()
    
    for char in s:
        if not(char in F):
            F[char] = 1
        else:
            F[char] += 1

    return F
    
def get_frequencies_from_file(file_name):
    """
    Computes a frequency table from the text in file_name.
    
    Parameters:
        file_name: The name of a text file.
        
    Returns:
        A frequency table F such that F[c] = (# of occurrences of c in the contents of <file_name>).
    """
    f = open(file_name, "r")
    s = f.read()
    f.close()

    return get_frequencies(s)

#Driver Code
F = get_frequencies_from_file("gettysburg-address.txt")
huff = HuffmanCode(F)
f = open("gettysburg-address.txt", "r")
s = f.read()
s = huff.encode(s)
print(s)
s = huff.decode(s)
print(s)