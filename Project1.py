"""
This file holds the shell and runs the program
    User can choose to run with or without an input file
---------------------

"""
import sys
from manager import Manager







def shell():
    # read in command line arguments to load in
    # python test.txt or smth

    output = open("outfile.txt", "w")
    output = open("outfile.txt", "a")


    if len(sys.argv) == 2  and sys.argv[1] is not None:
        with open(sys.argv[1], 'r') as file:
            lines = file.readlines()
        for line in lines:
            s = line.rstrip().split(" ")
            if (s[0] == "in"):
                manager = Manager(output, True)
            elif (s[0] == "cr"):
                manager.create(int(s[1]))
            elif (s[0] == "de"):
                manager.destroy(int(s[1]))
            elif(s[0] == "rq"):
                manager.request(int(s[1]), int(s[2]))
            elif (s[0] == "rl"):
                manager.release(int(s[1]), int(s[2]))
            elif (s[0] == "to"):
                manager.timeout()


    else:

        while True:
            print("> ", end="")
            s = input()
            s = s.rstrip().split(" ")
            if (s[0] == "in"):
                manager = Manager(outfile=None, mode=False)
            elif (len(s) == 2 and s[0] == "cr" and s[1] is not None):
                manager.create(int(s[1]))
            elif (len(s) == 2 and s[0] == "de" and s[1] is not None):
                manager.destroy(int(s[1]))
            elif (len(s) == 3 and s[0] == "rq" and s[1] is not None):
                manager.request(int(s[1]), int(s[2]))
            elif (len(s) == 3 and s[0] == "rl" and s[1] is not None ):
                manager.release(int(s[1]), int(s[2]))
            elif (s[0] == "to"):
                manager.timeout()
            elif (s[0] == "ready"):
                manager.printRL()
            elif (s[0] == "pcb"):
                manager.printPCB()
            elif (s[0] == "rcb"):
                manager.printRCB()



if __name__ == "__main__":
    shell()