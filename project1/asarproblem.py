#!/usr/bin/env python3.6

from aimapython.search import Problem
import sys


class ASARProblem(Problem):
    legs_left = 0
    legs = []
    classes= []

    def __init__(self):
        #self.initial =  # place here the initial state (or None)
        pass

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def goal_test(self, state):
        pass

    def path_cost(self, c, state1, action, state2):                         # path cost g(n)
        pass

    def heuristic(self, node):                                              # heuristic function h(n)
        # note: use node.state to access the state
        pass

    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        pass

    def save(self, fh, state):
        # note: fh is an opened file object
        pass


def load_problem(filename):
    with open(filename) as fh:
        lines = fh.readlines()
    return lines


def process(lines):
    A=[]
    P=[]
    L=[]
    C=[]

    for ln in lines:
            if ln[0] == 'A':
                A.append([s for s in ln.split() ])

            if ln[0] == 'P':
                P.append([s for s in ln.split()])

            if ln[0] == 'L':
                L.append([s for s in ln.split()])

            if ln[0] == 'C':
                C.append([s for s in ln.split()])
    for a in A:
        a[2] = int(a[2])
        a[3] = int(a[3])
    for l in L:
        l[3] = int(l[3])
        l[5] = int(l[5])
        l[7] = int(l[7])
    for c in C:
        c[2] = int(c[2])
    return [A, P, L, C]



def main():
    #prob = ASARProblem()
    #astar_search(prob)

    if len(sys.argv) > 1:
        lines = load_problem(sys.argv[1])
        #print(lines)
        [A, P, L, C] = process(lines)


    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()