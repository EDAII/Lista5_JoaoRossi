import sys
import random


class Node():
    def __init__(self, data):
        self.data = data  # node key
        self.parent = None # parent
        self.left = None # left child
        self.right = None # right child
        self.color = 1 # node color


class RedBlackTree():
    def __init__(self):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def pre_order_helper(self, node):
        if node != NULL:
            sys.stdout.write(node.data + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != NULL:
            self.in_order_helper(node.left)
            sys.stdout.write(node.data + " ")
            self.in_order_helper(node.right)

    def post_order_helper(self, node):
        if node != NULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(node.data + " ")

    def search_tree_helper(self, node, key):
        if node == NULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def fix_delete(self, value_x):
        while value_x != self.root and value_x.color == 0:
            if value_x == value_x.parent.left:
                s = value_x.parent.right
                if s.color == 1:
                    s.color = 0
                    value_x.parent.color = 1
                    self.rotate_left(value_x.parent)
                    s = value_x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    value_x = value_x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.rotate_right(s)
                        s = value_x.parent.right

                    # case 3.4
                    s.color = value_x.parent.color
                    value_x.parent.color = 0
                    s.right.color = 0
                    self.rotate_left(value_x.parent)
                    value_x = self.root
            else:
                s = value_x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    value_x.parent.color = 1
                    self.rotate_right(value_x.parent)
                    s = value_x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    value_x = value_x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.color = 1
                        self.rotate_left(s)
                        s = value_x.parent.left 

                    # case 3.4
                    s.color = value_x.parent.color
                    value_x.parent.color = 0
                    s.left.color = 0
                    self.rotate_right(value_x.parent)
                    value_x = self.root
        value_x.color = 0

    def rb_transplant(self, uncle, value):
        if uncle.parent == None:
            self.root = value
        elif uncle == uncle.parent.left:
            uncle.parent.left = value
        else:
            uncle.parent.right = value
        value.parent = uncle.parent

    def del_nh(self, node, key):
        # find the node containing key
        value_z = self.NULL
        while node != self.NULL:
            if node.data == key:
                value_z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if value_z == self.NULL:
            print ("Couldn't find key in the tree")
            return

        value_y = value_z
        y_original_color = value_y.color
        if value_z.left == self.NULL:
            value_x = value_z.right
            self.rb_transplant(value_z, value_z.right)
        elif (value_z.right == self.NULL):
            value_x = value_z.left
            self.rb_transplant(value_z, value_z.left)
        else:
            value_y = self.minimum(value_z.right)
            y_original_color = value_y.color
            value_x = value_y.right
            if value_y.parent == value_z:
                value_x.parent = value_y
            else:
                self.rb_transplant(value_y, value_y.right)
                value_y.right = value_z.right
                value_y.right.parent = value_y

            self.rb_transplant(value_z, value_y)
            value_y.left = value_z.left
            value_y.left.parent = value_y
            value_y.color = value_z.color
        if y_original_color == 0:
            self.fix_delete(value_x)
    
    def  fix_insert(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left # uncle
                if uncle.color == 1:
                    # case 3.1
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotate_left(node.parent.parent)
            else:
                uncle = node.parent.parent.right

                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent 
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.rotate_right(node.parent.parent)
            if node == self.root:
                break
        self.root.color = 0

    def print_helper(self, node, indent, last):
        if node != self.NULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("RIGHT->")
                indent += "     "
            else:
                sys.stdout.write("LEFT->")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print (str(node.data) + " (" + s_color + ") ")
            self.print_helper(node.left, indent, False)
            self.print_helper(node.right, indent, True)
    
    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, node):
        return self.search_tree_helper(self.root, node)

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node

    def successor(self, value_x):

        if value_x.right != self.NULL:
            return self.minimum(value_x.right)

        value_y = value_x.parent
        while value_y != self.NULL and value_x == value_y.right:
            value_x = value_y
            value_y = value_y.parent
        return value_y

    def predecessor(self,  value_x):

        if (value_x.left != self.NULL):
            return self.maximum(value_x.left)

        value_y = value_x.parent
        while value_y != self.NULL and value_x == value_y.left:
            value_x = value_y
            value_y = value_y.parent

        return value_y

    def rotate_left(self, value_x):
        value_y = value_x.right
        value_x.right = value_y.left
        if value_y.left != self.NULL:
            value_y.left.parent = value_x

        value_y.parent = value_x.parent
        if value_x.parent == None:
            self.root = value_y
        elif value_x == value_x.parent.left:
            value_x.parent.left = value_y
        else:
            value_x.parent.right = value_y
        value_y.left = value_x
        value_x.parent = value_y

    def rotate_right(self, value_x):
        value_y = value_x.left
        value_x.left = value_y.right
        if value_y.right != self.NULL:
            value_y.right.parent = value_x

        value_y.parent = value_x.parent
        if value_x.parent == None:
            self.root = value_y
        elif value_x == value_x.parent.right:
            value_x.parent.right = value_y
        else:
            value_x.parent.left = value_y
        value_y.right = value_x
        value_x.parent = value_y

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1 

        value_y = None
        value_x = self.root

        while value_x != self.NULL:
            value_y = value_x
            if node.data < value_x.data:
                value_x = value_x.left
            else:
                value_x = value_x.right

        node.parent = value_y
        if value_y == None:
            self.root = node
        elif node.data < value_y.data:
            value_y.left = node
        else:
            value_y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root

    def delete_node(self, data):
        self.del_nh(self.root, data)

    def print_tree(self):
        self.print_helper(self.root, "", True)

if __name__ == "__main__":
    red_black_tree = RedBlackTree()
    print(" ____  ____ _____")          
    print("|  _ \| __ )_   _| __ ___  ___ ")
    print("| |_) |  _ \ | || '__/ _ \/ _ \ ")
    print("|  _ <| |_) || || | |  __/  __/")
    print("|_| \_\____/ |_||_|  \___|\___|\n\n")
    
    print("Do you want to do it manually or automatic? ")
    option = input()

    if option == "manual":
        n = int(input("Enter the size of your Tree: "))

        for i in range(n):
            value = int(input("Enter the value to insert in your tree: "))
            red_black_tree.insert(value)
    
    else:
        for i in range(random.randint(2, 100)):
            red_black_tree.insert(random.randint(0, 1000))


    red_black_tree.print_tree()
