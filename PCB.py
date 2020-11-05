"""
This file contains the code required for the PCB data structure
---------------------

"""
from LinkedNode import LinkedNode

READY = 1
BLOCKED = 0


class PCB:
    def __init__(self, pid, parent = None, prio = 1, ):
        # only need to explicitly state if process is ready - 1 or blocked -0
        self.state = READY

        # if this process is a child process its parent will be located here
        if (parent is not None):
            self.parent = parent
        self.pid = pid
        self.priority = prio
        self.children = None
        self.resources = None

    def __str__(self):
        string = ""
        string += str(self.pid) + " -prio: " +  str(self.priority) + " -state: "
        if self.state ==BLOCKED:
            string += " blocked"
        else:
            string += "ready"
        string += " -children: "
        node = self.children
        while (node != None):
            string += str(node.value) + "->"
            node = node.next

        string += " -resources: "
        node = self.resources
        while (node != None):
            string += str(node.value) + "->"
            node = node.next

        return string



    def hasChild(self, j):
        node = self.children
        if node is None:
            return False
        else:
            while node is not None:
                if node.value == j:
                    return True
                node = node.next
            return False

    def insertChild(self, j):
        node = self.children
        if node is None:
            self.children = LinkedNode(j)
        else:
            while node.next != None:
                node = node.next
            node.next = LinkedNode(j)


    def removeChild(self, j):

        node = self.children # give it head of

        if node.getValue() == j:
            if node.next is not None:
                self.children = node.next
                node = None
            else:
                self.children = None
            return

        while node.next is not None:
            if node.next.getValue() == j:
                newNext = node.next.next
                if newNext is not None:
                    node.next = newNext
                else:
                    node.next = None
                return



    def getParent(self):
        return self.parent

    def getChildrenIds(self):
        children = set()
        node = self.children
        while node is not None:
            children.add(node.value)
            node = node.next
        return children

    """check if a resource id is in PCB - if so return -1"""

    def hasResource(self, rid):
        node = self.resources
        while node is not None:
            if node.value[0] == rid:
                return node.value[1]
            node = node.next
        return -1

    def insertResource(self, r, k):
        node = self.resources
        if(node is None):
            self.resources = LinkedNode(value=(r, k),next=None)

        else:
            while node.next != None:
                node = node.next
            node.next = LinkedNode(value=(r,k), next=None)

    def addToResource(self, j, k):
        node = self.resources
        while node is not None:
            if node.value[0] == j:
                node.value = (j,node.value[1]+k)
                break
            node=node.next
    def removeAllResource(self, rid):

        node = self.resources  # give it head of

        if node.value[0] == rid:
            amount_returned = node.value[1]
            if node.next is not None:
                self.resources = node.next
                node = None
            else:
                self.resources = None
            return amount_returned

        while node.next is not None:
            if node.next.getValue()[0] == rid:
                amount_returned = node.next.value[1]
                newNext = node.next.next
                if newNext is not None:
                    node.next = newNext
                else:
                    node.next = None
                return amount_returned
            node = node.next
        return -1

    def removeResource(self, rid, number):

        node = self.resources  # give it head of

        if node.value[0] == rid:

            a = node.value[1] - number
            node.value = (rid, a)
            if node.next is not None:
                self.resources = node.next
                node = None
            else:
                self.resources = None
            return number

        while node.next is not None:
            if node.next.getValue()[0] == rid:
                a = node.next.value[1] - number
                node.value = (rid, a)
                newNext = node.next.next
                if newNext is not None:
                    node.next = newNext
                else:
                    node.next = None
                return number
            node = node.next
        return -1

    def getPID(self):
        return self.pid

    def getPriority(self):
        return self.priority


    def setState(self, state):
        self.state = state

