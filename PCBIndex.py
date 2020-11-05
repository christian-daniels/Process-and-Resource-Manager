"""
This file contains the code for the container of PCBs
    It ensures accessing and manipulation of PCBs is done respectfully
    Also, it maintains cleanup of possible holes within itself
---------------------

"""
from PCB import PCB
from RL import RL


class PCBIndex:
    """
        Each process is represented by a data structure called the process control block (PCB).
        The PCBs are organized as a fixed-size array, PCB[n], where n is the maximum number of processes that can be created.
    """
    def __init__(self, size=16):

        self.process_list = [None] * size
        self.count = 1              # tracks total number of processes created
        self.current = 1            # tracks current number of processes in PCB
        self.exists_list = set()    # quicker way to check if a process exists in the list O(1)
        self.start()

    def start(self):
        # when the PCB is initalized process 0 is started
        self.process_list[0] = PCB(pid=0, prio=0)
        self.exists_list.add(0)
        return

    """
    Creates a new process in the PCB
    """
    def create(self, prio, parent):

        self.process_list[self.current] = PCB(pid=self.count, parent=parent, prio=prio)
        self.exists_list.add(self.count)
        self.current += 1
        self.count += 1

        return self.count - 1

    # after destroying, reshuffle to rid of empty spots
    def reshuffle(self):
        alist = []
        for i in self.process_list:
            if i is not None:
                alist.append(i)

        self.process_list = [None] * 16
        for i, p in enumerate(alist):
            self.process_list[i] = p
            self.current = i+1

    def accessProcessChild(self, parent_index : int, pid : int):
        self.process_list[parent_index].insertChild(pid)

    def accessProcessHasResource(self, process_index : int, rid : int):
        return self.process_list[process_index].hasResource(rid)

    def addProcessResource(self, process_index : int, rid : int, numUnits : int):
        self.process_list[process_index].insertResource(r=rid, k=numUnits)

    def appendProcessResource(self,process_index : int, rid : int, numUnits : int):
        self.process_list[process_index].addToResource(rid,numUnits)

    def accessProcessState(self, process_index : int, state : int):

        self.process_list[process_index].setState(state)

    def releaseAllResource(self, process_index : int, rid : int):
        return self.process_list[process_index].removeAllResource(rid)

    def releaseResource(self, process_index : int, rid : int, number_to_release):
        return self.process_list[process_index].removeResource(rid, number_to_release)


    def remove(self, parent_id : int, to_be_deleted_id : int):
        num_deleted = 0
        tbd_index = self.find(to_be_deleted_id)
        # remove all children and their children
        set_of_children = self.process_list[tbd_index].getChildrenIds()
        current = set(set_of_children)
        if (len(set_of_children) >0):
            for child in set_of_children:
                num, new_set = self.remove(to_be_deleted_id, child)
                num_deleted += num
                current.update(new_set)

        return 1 + num_deleted, current

    def removeFromParent(self, parent_id : int, to_be_removed_id : int):
        parent_index = self.find(parent_id)
        self.exists_list.remove(to_be_removed_id)
        if parent_index is not None:
            self.process_list[parent_index].removeChild(to_be_removed_id)

    def removeFromRL(self, ready_list : RL, to_be_deleted_id : int):
        ready_list.remove(j=to_be_deleted_id)
        return ready_list

    def checkIsValid(self, parent_id, pid):
        # cases
            # 1. parent_id is pid
            # 2. pid is in parent_id children
        if(parent_id is pid):
            return True
        else:
            index = self.find(parent_id)
            return self.process_list[index].hasChild(pid)

    """
    Returns the index of the desired process
    """
    def find(self, pid):
        for i, p in enumerate(self.process_list):
            # if self.process_list[i] is None:
            #     break
            if self.process_list[i] is None:
                continue
            elif self.process_list[i].getPID() == pid:
                return i


    def exists(self, pid):
        return pid in self.exists_list

    """
    Returns the # of processes created
    """
    def getCount(self):
        return self.count

    """
    Returns the # of processes currently inside the PCB
    """
    def getCurrent(self):
        return self.current
    def adjustCount(self, numProcesses):
        self.count -= numProcesses