"""
This file holds the Process and Resource Manager
    It runs the main commands given a certain input from the shell
---------------------

"""

from PCBIndex import PCBIndex
from RCBIndex import RCBIndex
from RL import RL

# Constants
READY = 1
BLOCKED = 0
SIZE = 16


class Manager:

    def __init__(self, outfile, mode=True):
        # A process descriptor array PCB[16]
        # A resource descriptor array RCB[4] with multiunit resources
        # RCB[0] and RCB[1] have 1 unit each; RCB[2] has 2 units; RCB[3] has 3 units
        #   A 3-level RL
        self.PCBIndex = PCBIndex()
        self.RL = RL()
        self.RCBIndex = RCBIndex()
        self.n = SIZE
        self.mode = mode
        if self.mode:
            self.output = outfile # o
        # this is the process at the head of RL

        # Erase all previous contents of the data structures PCB, RCB, RL
        self.start()

    """
    start(): The init function should always perform the following tasks:
                Create a single running process at PCB[0] with priority 0
                Enter the process into the RL at the lowest-priority level 0
                self.PCB._process_list[0] = Process(pid=0, prio=0)
    """
    def start(self):

        self.PCBIndex.start()
        self.runningid = 0
        self.RL.enqueue(pid=0, priority=0)
        if self.mode:
            self.output.write("\n")
        self.scheduler()

    """
    create(): a new process is created once and is given a unique id, a parent, and a priority
                a context switch is ran in case the new process has a higher priority
    """
    def create(self, priority: int):
        if (1 <= priority <= 2):

            if self.PCBIndex.getCurrent() >= self.n:
                self.displayError()
            else:
                pid = self.PCBIndex.create(priority, parent=self.runningid)
                parent_index = self.PCBIndex.find(self.runningid)
                self.PCBIndex.accessProcessChild(parent_index, pid)
                self.RL.enqueue(pid=pid, priority=priority)
                # print("process", pid, "created")
                # print(pid)
                self.scheduler()
        else:
            self.displayError()


    """
    destroy(): removes a process and its children from the program. This includes the deletion of its PCB,
                removal from the ReadyList, releasing of possible resources, and the cleansing of a resources
                WaitList
    """
    def destroy(self, j):
        if j == 0: # EXCEPTION - attempt to delete process 0
            self.displayError()
        elif self.PCBIndex.checkIsValid(parent_id=self.runningid, pid=j):
            # find the set of children process may have
            total, set_of_children = self.PCBIndex.remove(self.runningid, j)  # for all k in j destroy(k)
            # destroy children
            for pid in set_of_children:
                tbd_index = self.PCBIndex.find(pid)

                a = self.PCBIndex.process_list[tbd_index].resources
                while a is not None:
                    self.releaseInDestroy(a.value[0], pid)
                    a = a.next
                if self.PCBIndex.exists(pid):
                    self.PCBIndex.removeFromParent(self.PCBIndex.process_list[tbd_index].getParent(), pid)
                self.RL.remove(decision=False, j=pid)
                self.PCBIndex.process_list[tbd_index] = None

            # destroy j - remove j from its parent, ready list,
            tbd_index = self.PCBIndex.find(j)
            a = self.PCBIndex.process_list[tbd_index].resources
            if self.PCBIndex.exists(j):
                self.PCBIndex.removeFromParent(self.PCBIndex.process_list[tbd_index].getParent(), j)
            while a is not None:
                self.releaseInDestroy(a.value[0], j)
                a = a.next
            self.RL.remove(decision=False, j=j)
            self.PCBIndex.process_list[tbd_index] = None

            # run through RCBs waitinglist to remove possible waiting processes
            alist = list(set_of_children)
            alist.append(j)
            self.RCBIndex.cleanseWaitlist(alist)

            # fix PCBindex in case there are any gaps
            self.PCBIndex.reshuffle()

            self.scheduler()

        else: # EXCEPTION - attempt to delete a process that is not there
            self.displayError()


    """
    request(): the running process makes an attempt to request a number of units from a given resource
                if the resource has the number of requested units available, it is allocated to the running process
                if the resource does not have the units available, the running process is removed from the ReadyList,
                its state is set to Blocked, and is placed on the requested resource's WaitList
    """
    def request(self, resource, numUnits):
        if resource < 0 or resource > 3:
            self.displayError()
            return
        refResource = self.RCBIndex.getResource(resource)

        if (self.runningid == 0):  # EXCEPTION - requesting resource for process 0
            self.displayError()
        elif (numUnits == 0):   # requesting 0 units is not an exception but it does nothing
            self.scheduler()
            return  # this refers to piazza post: https://piazza.com/class/kffw9nufy3m5qf?cid=35
        elif (refResource == -1):  # EXCEPTION - nonexistent resource
            self.displayError()
        elif (refResource.state >= numUnits):
            value = self.PCBIndex.accessProcessHasResource(process_index=self.PCBIndex.find(self.runningid),
                                                           rid=resource)
            if value != -1:  # has resource and can append it
                self.PCBIndex.appendProcessResource(process_index=self.PCBIndex.find(self.runningid), rid=resource,
                                                    numUnits=numUnits)
                self.RCBIndex.setResource(rid=resource, k=numUnits, change=True)
                self.scheduler()
            else:  # doesnt have resource and can add it to its resource list

                self.RCBIndex.setResource(rid=resource, k=numUnits, change=True)
                parent_index = self.PCBIndex.find(self.runningid)
                self.PCBIndex.addProcessResource(process_index=parent_index, rid=resource, numUnits=numUnits)
                self.scheduler()
                # print("received", numUnits, "units")
        else:
            value = self.PCBIndex.accessProcessHasResource(process_index=self.PCBIndex.find(self.runningid),
                                                           rid=resource)
            if value != -1:
                # process has resource we must add the prexisting value to the numUnits the resource has requested
                if numUnits > refResource.inventory: # EXCEPTION - process is requesting more than what a resource initially has
                    self.displayError()
                elif (value + numUnits) > refResource.inventory:  # EXCEPTION - process is requesting more than what a resource has
                    self.displayError()
                else:
                    parent_index = self.PCBIndex.find(self.runningid)
                    self.PCBIndex.accessProcessState(process_index=parent_index, state=0)
                    self.RL.remove(decision=True, j=self.runningid)
                    self.RCBIndex.enqueue(rid=resource, i=self.runningid, k=numUnits)
                    self.scheduler()
            else:
                if numUnits > refResource.inventory: # EXCEPTION - process is requesting more than what a resource initially has
                    self.displayError()
                    return
                parent_index = self.PCBIndex.find(self.runningid)
                self.PCBIndex.accessProcessState(process_index=parent_index, state=0)
                self.RL.remove(decision=True, j=self.runningid)
                self.RCBIndex.enqueue(rid=resource, i=self.runningid, k=numUnits)
                self.scheduler()


    """
    release(): releases the desired resources 
    """
    def release(self, resource, number):
        # check if resource is allocated to running process
        if resource < 0 or resource > 3:
            self.displayError()
            return

        value = self.PCBIndex.accessProcessHasResource(process_index=self.PCBIndex.find(self.runningid), rid=resource)

        if value == -1 or value < number: # EXCEPTION - Releasing a resource the process is not holding
            self.displayError()
        elif number == 0: # not exception, but attempt to release 0 units does nothing
            self.scheduler()
            return
        else:
            # remove r from resources list of process i
            amount_to_add = self.PCBIndex.releaseResource(self.PCBIndex.find(self.runningid), resource, number)
            # add amount released back into resource
            self.RCBIndex.setResource(resource, amount_to_add, False)
            refResource = self.RCBIndex.getResource(resource)
            if refResource.waiting_list is None:
                pass
            else:
                #  This only grabs looks at one spot in waitinglist
                while(self.RCBIndex.peek(resource)):

                    pid, amount = self.RCBIndex.dequeue(resource)
                    process_index = self.PCBIndex.find(pid)
                    self.PCBIndex.accessProcessState(process_index, 1)
                    self.RCBIndex.setResource(resource, amount, True)
                    # check if process has the resource
                    if self.PCBIndex.accessProcessHasResource(process_index, resource) != -1:
                        self.PCBIndex.appendProcessResource(process_index, resource, amount)
                    else:
                        self.PCBIndex.addProcessResource(process_index, resource, amount)

                    self.RL.enqueue(pid, self.PCBIndex.process_list[process_index].getPriority())
            # print("resource", str(resource), "released")
            self.scheduler()


    """
    timeout(): performs a purposeful context switch
    """
    def timeout(self):
        # moves running process to the end of their priority level
        # calls scheduler at the end
        self.RL.timeout()
        self.scheduler()

    """
    scheduler(): retrieves the highest priority process 
                used for context switches
    """
    def scheduler(self):
        # if (self.RL.findHead() != -1):
            # print("process " + str(self.RL.getHead()) + " is running")
            # print(str(self.RL.getHead()))
        self.RL.findHead()
        self.runningid = self.RL.getHead()
        if self.mode:
            self.output.write(str(self.runningid) + " ")
        else:
            print(str(self.RL.getHead()))

    """
    Helper Functions: functions that are not explicitly required but are needed to run required ones
    """
    def displayError(self):
        if self.mode:
            self.output.write(str(-1) + " ")
        else:
            print(-1)
    def releaseInDestroy(self, resource, from_pid):
        value = self.PCBIndex.accessProcessHasResource(process_index=self.PCBIndex.find(from_pid), rid=resource)

        if value == -1: # Exceptions: Releasing a resource the process is not holding
            # print(-1)
            self.displayError()
        else:
            amount_to_add = self.PCBIndex.releaseAllResource(self.PCBIndex.find(from_pid), resource) # remove r from resources list of process i
            self.RCBIndex.setResource(resource, amount_to_add, False) # add amount released back into resource
            refResource = self.RCBIndex.getResource(resource)
            if refResource.waiting_list is None:
                pass
            else:
                pid, amount = self.RCBIndex.dequeue(resource)
                process_index = self.PCBIndex.find(pid)
                if process_index != -1 and process_index != None:
                    self.PCBIndex.accessProcessState(process_index, 1)
                    self.RCBIndex.setResource(resource, amount, True)
                    # check if process has the resource
                    if self.PCBIndex.accessProcessHasResource(process_index, resource) != -1:
                        self.PCBIndex.appendProcessResource(process_index, resource, amount)
                    else:
                        self.PCBIndex.addProcessResource(process_index, resource, amount)

                    self.RL.enqueue(pid, self.PCBIndex.process_list[process_index].getPriority())
            # print("resource", str(resource), "released")
            # self.scheduler()

    """
    DEBUG Functions
    """
    def printRL(self):
        node = self.RL.readylist
        print("printRL")
        for i in range(0, 3):
            print("\nin " + str(i), end=" ")
            node = self.RL.readylist[i]
            while (node != None):
                print(str(node.value) + "->", end='')
                node = node.next
        print()

    def printPCB(self):
        print("print PCB")
        for i in range(self.PCBIndex.getCurrent()):
            print("Id: " + str(self.PCBIndex.process_list[i]))

    def printRCB(self):
        print("print RCB")
        for i in range(0, 4):
            print("Id: " + str(self.RCBIndex.resource_list[i]))
