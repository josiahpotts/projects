# Name: Josiah Potts
# Modified Date: 7/25/2022
# Description: Using the BST data structure to operate and access data.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object, current_node = None) -> None:
        """
        Method: add()
        Parameters: value: object, current_node = None
        Returns: current_node
        Description: This method uses recursion to traverse through the BST, moving left and right of nodes based
                    on the input value, and adds the value to the correct spot of the tree once the current node's
                    child on the proper side reads None.
        """
        #Upon first call the paramenter of current_node will be set to the root.
        if current_node == None:
            current_node = self._root

        #Base case.
        if self._root == None:
            self._root = BSTNode(value)
            return
        #If head has a node.
        else:
            #Move left.
            if value < current_node.value:
                if current_node.left == None:
                    current_node.left = BSTNode(value)
                else:
                    #Check left and right at the left node by calling add() recursively.
                    current_node.left = self.add(value, current_node.left)
            #Move right.
            elif value >= current_node.value:
                if current_node.right == None:
                    current_node.right = BSTNode(value)
                else:
                    #Check left and right at the right node by calling add() recursively.
                    current_node.right = self.add(value, current_node.right)

        #Return current working node for recusive functions.
        return current_node

    def find(self, value: object) -> object:
        """
        Method: find()
        Parameters: value: object
        Returns: object
        Description: Traverse the BST to find the node that contains the desired value.
        """
        #Initialize node for traversal.
        node = self._root

        #Iterate through BST and compare node values to value.
        while node != None:
            if node.value == value:
                #If value is found return the node it is found in.
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right

        #Return False if value does not exist in the nodes.
        return False

    def find_parent(self, value: object) -> object:
        """
        Method: find_parent()
        Parameters: value: object
        Returns: object
        Description: Travers the BST to find the parent of the desired node for use in other functions. No checking
                    needed within function as values passed into the function will be checked outside of function.
        """
        #Initialize node and node parent for traversal.
        node = self._root
        np = None

        #Iterate through BST to compare the value, storing the node parent along the way.
        while node != None:
            if node.value == value:
                #If value is found return that node's parent.
                return np
            elif value < node.value:
                np = node
                node = node.left
            else:
                np = node
                node = node.right

    def check_for_children(self, node: BSTNode) -> int:
        """
        Method: check_for_children()
        Parameters: node: BSTNode
        Returns: int
        Description: Helper method for remove() to discover the removal situation. Returns int value that replicates
                    no child, left child, right child, or two children.
        """
        #Check if no children.
        if node.left == None and node.right == None:
            return 0
        #Check if left child.
        elif node.left != None and node.right == None:
            return -1
        #Check if right child.
        elif node.left == None and node.right != None:
            return 1
        #Check if two children.
        elif node.left != None and node.right != None:
            return 2

    def remove(self, value: object) -> bool:
        """
        Method: remove()
        Parameters: value: object
        Returns: bool
        Description: Uses helper method find() to find the requested node (if does not exist return false), and that node's
                    parent node. Using the node and parent node it will call other helper functions based on the removal
                    situation in order to successfully remove and restructure the BST.
        """
        #Initialize node and parent node to work with.
        node = self.find(value)
        np = self.find_parent(value)

        #If value does not exist in BST, return false.
        if node == False:
            return False
        #If removal node is a leaf call the _remove_no_subtrees() helper method.
        elif node.left == None and node.right == None:
            self._remove_no_subtrees(np, node)
            return True
        else:
            #Initialize the child situation for the node.
            children = self.check_for_children(node)
            #If there is one child.
            if children == -1 or children == 1:
                self._remove_one_subtree(np, node, children)
                return True
            #Handles if there are two children.
            elif children == 2:
                self._remove_two_subtrees(np, node)
                return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Method: _remove_no_subtrees()
        Parameters: remove_parent: BSTNode, remove_node: BSTNode
        Returns: None
        Description: Removes a node that is a leaf with no children.
        """
        #Remove node that has no subtrees (no left or right nodes)
        if remove_parent == None:
            self._root = None
            return
        if remove_parent.right == remove_node:
            remove_parent.right = None
        else:
            remove_parent.left = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode, child: int) -> None:
        """
        Method: _remove_one_subtree()
        Parameters: remove_parent: BSTNode, remove_node: BSTNode, child: int
        Returns: None
        Description: Handles the removal of a single child situation for passed node. Different handling for left
                    and for right children.
        """
        #Check base case that node to be removed is the root with one child.
        if remove_parent == None:
            if child == -1:
                self._root = remove_node.left
                return
            elif child == 1:
                self._root = remove_node.right
                return
        #Remove node that has a left or right subtree (only)

        #Check if node to remove is to the right of the parent.
        if remove_parent.right == remove_node:
            #Check if left child.
            if child == -1:
                remove_parent.right = remove_node.left
            #Check if right child.
            elif child == 1:
                remove_parent.right = remove_node.right
        #If not to the right then it is left of the parent.
        else:
            #Check if left child.
            if child == -1:
                remove_parent.left = remove_node.left
            #Check if right child.
            elif child == 1:
                remove_parent.left = remove_node.right

    def find_successor(self, node: BSTNode) -> object:
        """
        Method: find_successor()
        Parameters: node: BSTNode
        Returns: object
        Description: Helper method to find the in-order successor for the removal of a node in BST. If called this method
                    will reassign the successor's parent accordingly and return the successor node.
        """
        #Initialize removal node's right node and successor_parent for traversal.
        successor = node.right
        successor_parent = node

        #Traverse BST to the left most child to find in-order successor and its parent.
        while successor.left != None:
            successor_parent = successor
            successor = successor.left

        #Check if node to remove is the successor's parent to avoid losing nodes.
        if node != successor_parent:
            successor_parent.left = None

        #Check if successor has a right child and if so, assign it to the successor's parent.
        if successor.right != None:
            if node != successor_parent:
                successor_parent.left = successor.right

        #Return the successor node.
        return successor

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Method: _remove_two_subtrees()
        Parameters: remove_parent: BSTNode, remove_node: BSTNode
        Returns: None
        Description: Helper method if removal node has two children. Replaces that node location with successor, and
                    reorganizes affected nodes into proper place.
        """
        #Initialize successor to the removed node (Note: this will reassign the successor's right child).
        succ = self.find_successor(remove_node)

        #Special case: if node to remove is the root of the BST.
        if remove_node == self._root:
            #If successor is right child to root then no reassigning to the right is necessary.
            if remove_node.right != succ:
                succ.right = remove_node.right
                remove_node.right = None
            #Root's left child becomes the successor's left child.
            succ.left = remove_node.left
            #Cut the references from the removed node.
            remove_node.left = None
            #Set the new root to successor.
            self._root = succ
        #If node to remove is right of the parent.
        elif remove_parent.right == remove_node:
            #Important: If the removed node's right child is the successor it need not reassign.
            if remove_node.right != succ:
                succ.right = remove_node.right
            #Reassign the successor's left reference to the removed node's left reference.
            if succ != remove_node.left:
                succ.left = remove_node.left
            #Reassign parent node to point to new successor, skipping over removal node.
            remove_parent.right = succ
        #If node to remove is left of the parent.
        elif remove_parent.left == remove_node:
            #Successor's left reference will become the removal node's left.
            succ.left = remove_node.left
            #If right node of removal node is the successor, skip reassigning of right node.
            if succ != remove_node.right:
                succ.right = remove_node.right
            #Set parent node to point to new successor, skipping over removal node.
            remove_parent.left = succ

    def contains(self, value: object) -> bool:
        """
        Method: contains()
        Parameters: value: object
        Returns: bool
        Description: Call the helper find() method to traverse BST to find specific value. If value exists it returns
                    True, or if the value does not exist it returns False.
        """
        #Initialize if the value is found using the find() helper method.
        found = self.find(value)

        #Check the results of traversal.
        if found == False:
            return False
        else:
            return True

    def inorder_traversal(self, first_call = True, node = None, inorder = Queue()) -> Queue:
        """
        Method: inorder_traversal()
        Parameters: first_call = True, node = None, inorder = Queue()
        Returns: Queue
        Description: Creates a queue of the values inorder for the BST using recursive calls. Queue is emptied if
                    another queue request is made.
        """
        #Special case: Empty BST.
        if self._root == None:
            #Clear the queue if not empty.
            while inorder.is_empty()!= True:
                inorder.dequeue()
            return inorder
        #For initial call of the function. Set the node to the root for recursive calls.
        elif first_call == True:
            #Clear the queue if not empty.
            while inorder.is_empty() != True:
                inorder.dequeue()
            node = self._root

        #If node is empty, return from recursive call.
        if node == None:
            return inorder

        #If node is not empty, make recursive call to left until there is no left, then return values, then make recursive call to the right.
        if node:
            self.inorder_traversal(False, node.left, inorder)
            inorder.enqueue(node.value)
            self.inorder_traversal(False, node.right, inorder)

        #Return the queue.
        return inorder

    def find_min(self) -> object:
        """
        Method: find_min()
        Parameters: None
        Returns: object
        Description: Traverse to the farthest left node of the BST where the minimum value is held and return it.
        """
        #If BST is empty, return none.
        if self._root == None:
            return None
        #If root has no left node it is the minimum value.
        elif self._root.left == None:
            return self._root.value

        #Initialize starting node for traversal.
        node = self._root

        #Traverse as far left as able.
        while node.left != None:
            node = node.left

        #Farthest left node will be returned.
        return node.value

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        #If BST is empty, return none.
        if self._root == None:
            return None
        #If root has no left node it is the maximum value.
        elif self._root.right == None:
            return self._root.value

        #Initialize starting node for traversal.
        node = self._root

        #Traverse to the farthest right node.
        while node.right != None:
            node = node.right

        #Return the farthest right node which is the max.
        return node.value

    def is_empty(self) -> bool:
        """
        Method: is_empty()
        Parameters: None
        Returns: bool
        Description: Checks if there is a root node, if there is then the BST is not empty.
        """
        #Check if root is empty.
        if self._root == None:
            return True
        #If not empty return false.
        else:
            return False

    def make_empty(self) -> None:
        """
        Method: make_empty()
        Parameters: None
        Returns: None
        Description: Set root of BST to none, breaking access to any reference to BST and making it empty.
        """
        #Initialize BST root to None.
        self._root = None

# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
