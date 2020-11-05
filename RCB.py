"""
This file contains the code required for the RCB data structure

---------------------

"""
from LinkedNode import LinkedNode


class RCB:
    def __init__(self, id, numUnits):
        self.state = numUnits # integer counter, to keep track of how many units are still available
        self.inventory = numUnits # new field, inventory, indicates initial number of units (1, 2, or 3)
        self.id = id
        self.waiting_list = None # a queue - each element contains process index and number of units requested

    def __str__(self):
        string = ""
        string += str(self.id) + " -state: " + str(self.state) + " -inventory: " + str(self.inventory) + " -waiting: "
        node = self.waiting_list
        while (node != None):
            string += str(node.value) + "->"
            node = node.next
        return string

    def getRID(self):
        return self.id

    def takeResource(self):
        if (self.state != 0):
            # we return a
            pass
        else:
            return -1

    def enqueueWaitingList(self, i, k):
        node = self.waiting_list
        if (self.waiting_list == None):
            self.waiting_list = LinkedNode((i,k))
        else:

            while node.next != None:
                node = node.next
            node.next = LinkedNode((i, k))

    def dequeueWaitingList(self):

        temp = self.waiting_list
        self.waiting_list = self.waiting_list.next

        i = temp.value[0]
        k = temp.value[1]
        temp = None #delete the contents
        return (i, k)
    """
    RCB checks if its first element is dequeuable
    """
    def peek(self):
        if self.waiting_list is not None:
            return self.waiting_list.value[1] <= self.state
        return False
