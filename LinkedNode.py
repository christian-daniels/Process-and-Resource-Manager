"""
This file contains basic code for a Node of a LinkedList
---------------------

"""

class LinkedNode:
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

    def getValue(self):
        return self.value