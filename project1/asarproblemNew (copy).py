#!/usr/bin/env python3.6

from aimapython.search import astar_search
from aimapython.search import EightPuzzle
from aimapython.search import Problem
import sys


class Legs:
    #profit_list = []            #make some sort of dictionary or tuple?
    #class_list = []

    def __init__(self, leg, id):
        self.id = id                    #is the id needed?
        self.dep_airport = leg[1]
        self.arr_airport = leg[2]
        self.dur = leg[3]

        self.profits = { leg[i]:leg[i+1] for i in range(len(leg)) if i >= 4 and i%2 == 0 }

        """index = 0
        for fields in leg:
            if index >= 4 and index%2 == 0:
                self.class_list.append(fields[index])
                self.profit_list.append(fields[index+1])
            index=index+1"""

    def get_dur(self):
        return self.dur

    def get_arr_airport(self):
        return self.arr_airport

    def get_dep_airport(self):
        return self.dep_airport

    def get_profit(self, c):
        return self.profits[c]

    def get_id(self):
        return self.id


class Airplane:

    def __init__(self, plane, id):
        self.id = id
        self.name = plane[1]
        self.c = plane[2]
        self.location = -1
        self.time = 0

    def get_class(self):
        return self.c

    def get_location(self):
        return self.location

    def perform_leg(self, leg, airport_list, airClasses):
        self.location = leg.get_arr_airport()
        dep = leg.get_dep_airport()
        arr = leg.get_arr_airport()

        leg_dur = leg.get_duration()
        self.time = max(self.time + leg_dur, airport_list[dep][0] + leg_dur, airport_list[arr][0])
        self.time = self.time + airClasses[self.c]

    def get_id(self):
        return self.id

    def get_time(self):
        return self.time

    def set_time(self, delta):
        self.time = self.time + delta

    def set_location(self, location):
        self.location = location


class state:
    def __init__(self, legs_left, planes):
        self.legs_left = legs_left
        self.planes = planes


class ASARProblem(Problem):

    def __init__(self, filename):
        #self.initial =  # place here the initial state (or None)
        fh = open(filename)
        [A, P, L, C] = self.load(fh)

        self.airClasses = {C[i][0]:C[i][1] for i in range(len(C))}
        self.airports = {A[i][0]: (A[i][1], A[i][2]) for i in range(len(A))}    # verificar closing>opening???

        self.legs = [Legs(l, i) for l in L for i in range(0, len(L))]
        planes = [Airplane(p, i) for p in P for i in range(0, len(P))]

        needed_info = [[p.get_location() for p in planes], [p.get_time() for p in planes], [-1 for i in range(len(P))]]

        initial = (tuple([l.get_id() for l in self.legs]), tuple(tuple(i) for i in needed_info))

        #initial = state([l.get_id() for l in self.legs], [p.get_location() for p in planes])

        Problem.__init__(self, initial)


    def actions(self, state):
        # possible actions consist of applying a leg to a given plane
        possible_actions = [[, l] for p in state.planes for l in state[0]]

        for action in possible_actions:
            # pode-se otimizar fazendo pre-processamento

            # tem de começar onde o avião está
            if state.planes[action[0]].get_location() != self.legs[action[1]].get_dep_airport():
                possible_actions.remove(action)
                continue

            # parte a uma hora em que o departure airport já abriu
            """apt = self.legs[action[1]].get_dep_airport()
            if self.planes[action[0]].get_time() < self.airports[apt][0]:
                possible_actions.remove(action)
                continue
            """
            #chega a uma hora em que o arrival airport já abriu
            """apt = self.legs[action[1]].get_arr_airport()
            if self.planes[action[0]].get_time() + self.legs[action[1]].get_dur() < self.airports[apt][0]:
                possible_actions.remove(action)
                continue
            """
            # parte a uma hora em que o departure airport ainda não fechou
            apt = self.legs[action[1]].get_dep_airport()
            if state.planes[action[0]].get_time() > self.airports[apt][1]:
                possible_actions.remove(action)
                continue

            #chega a uma hora em que o arrival airport ainda não fechou
            apt = self.legs[action[1]].get_arr_airport()
            if state.planes[action[0]].get_time() + self.legs[action[1]].get_dur() > self.airports[apt][1]:
                possible_actions.remove(action)
                continue

        return possible_actions"""

    def result(self, state, action):
        state.legs_left.remove(action[1])
        state.planes[action[0]].perform_leg(self.legs[action[1]])

    def goal_test(self, state):
        pass

    def path_cost(self, c, state1, action, state2):                         # path cost g(n)
        profit = self.legs[action[1]].get_profit(state1.planes[action[0]].get_class())
        return c + 1/profit

    def heuristic(self, node):                                              # heuristic function h(n)
        # note: use node.state to access the state
        # numero de avioes deslocados + numero de legs que faltam
        #return len(node.state.legs_left) +
        pass

    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        lines = fh.readlines()
        return process(lines)



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

    if len(sys.argv) > 1:
        prob = ASARProblem(sys.argv[1])
        # astar_search(prob)
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()






""" puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))
    sol = astar_search(puzzle)
    print("parent ", sol.parent, "state ", sol.state, "action ", sol.action, "path cost ", sol.path_cost, "depth ", sol.depth)
    print("grandpa", sol.parent.parent)"""


