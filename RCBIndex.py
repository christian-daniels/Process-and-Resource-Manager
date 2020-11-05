"""
This file contains the code for the container of RCBs
    It ensures accessing and manipulation of RCBs is done respectfully
---------------------

"""
from RCB import RCB


class RCBIndex:
    def __init__(self):
        self.resource_list = [None]*4
        self.start()

    def start(self):
        for i in range(0,4):
            if (i == 0 or i == 1):
                self.resource_list[i] = RCB(id=i, numUnits=1)
            if (i == 2):
                self.resource_list[i] = RCB(id=i, numUnits=2)
            if (i == 3):
                self.resource_list[i] = RCB(id=i, numUnits=3)

    def getResource(self, rid : int):
        return self.resource_list[rid]
    def setResource(self, rid : int, k : int, change : bool):
        if(change):
            self.resource_list[rid].state -= k
        else:
            self.resource_list[rid].state += k
    def enqueue(self, rid : int, i : int, k : int):
        self.resource_list[rid].enqueueWaitingList(i,k)

    def dequeue(self, rid : int):
        return self.resource_list[rid].dequeueWaitingList()

    def peek(self, rid : int):
        return self.resource_list[rid].peek()
    def cleanseWaitlist(self, process_list):
        for i,resource in enumerate(self.resource_list):
            node = resource.waiting_list

            if node == None:
                continue
            if node.getValue()[0] in process_list:
                if node.next is not None:
                    self.resource_list[i].waiting_list = node.next
                    node = None
                else:
                    self.resource_list[i].waiting_list = None

            if node.next is not None:
                while node.next is not None:
                    if node.next.getValue()[0] in process_list:
                        newNext = node.next.next
                        if newNext is not None:
                            node.next = newNext
                        else:
                            node.next = None
                        node = node.next

