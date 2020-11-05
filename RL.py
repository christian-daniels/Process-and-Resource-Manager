"""
This file contains the code required for the RL data structure
    maintains finding the head, the process with the highest priority and is assumed to be running
---------------------

"""
from LinkedNode import LinkedNode


class RL:
    def __init__(self):
        # readylist is a list of 3 Linked lists
        # level 2 is the highest, 0 the lowest
        self.readylist = [None]*3
        self.head = -1
        # self.head # this keeps track of the process that will be run next


    def getHead(self):
        return self.head.value

    def findHead(self):
        answer = None
        for i in range(len(self.readylist)-1, -1, -1):
            if self.readylist[i] != None:
                answer = self.readylist[i]
                break

        self.head = answer
        return answer.value if answer != None else -1

    def enqueue(self, pid : int, priority: int):

        if(self.readylist[priority] == None):
            self.readylist[priority] = LinkedNode(pid)
        else:
            # loop through that prio level and find the end
            node = self.readylist[priority]
            while node.next != None:
                node = node.next
            node.next = LinkedNode(value=pid,next=None)





    def remove(self, decision ,j):
        if decision:
            # set the head to none - we will find a new head with scheduler
            self.head = None
            self.remove(decision=False,j=j)
        else:
            for prio_level in range(len(self.readylist) - 1, -1, -1):
                if self.readylist[prio_level] != None:
                    node = self.readylist[prio_level]
                    if node.getValue() == j:
                        if node.next is not None:
                            self.readylist[prio_level] = node.next
                            node = None
                        else:
                            self.readylist[prio_level] = None
                        return

                    while node.next is not None:
                        if node.next.getValue() == j:
                            newNext = node.next.next
                            if newNext is not None:
                                node.next = newNext
                            else:
                                node.next = None
                            return
                        node = node.next










    def timeout(self):
        # moves running process (head) to the end of its priority level
        # we have head
        # we have to set head->next to head if head == None
        #find the prio level head is in
        for i in range(len(self.readylist)-1, -1, -1):
            if self.readylist[i] != None:
                answer = i
                break
        node = self.readylist[answer]
        node = node.next
        if(node != None):
            self.enqueue(self.head.value, answer)
            self.readylist[answer] = node



            # leave it alone
