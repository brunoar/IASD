#!/usr/bin/env python3.6


from aimapython.search import astar_search
from aimapython.search import EightPuzzle
from aimapython.search import Problem
import sys


class Legs:
    dep_airport = []
    arr_airport = []
    dur = []
    profit_list = []
    class_list = []

    def __init__(self, legs_list):
        index = 0
        for leg in legs_list:
            self.dep_airport.append(leg[1])
            self.arr_airport.append(leg[2])
            self.dur.append(leg[3])
            for fields in leg:
                if index >= 4 and index%2 == 0:
                    self.class_list.append(fields[index])
                    self.profit_list.append(fields[index+1])
                index=index+1

    """def get_dep_airport(self,legs):
        index = self.dep_airport.index(airport)
        return self.dep[index]
    """

    def get_arr_airport(self, dep):
        index = [i for i, x in enumerate(self.dep_airport) if self.dep_airport == dep]
        return self.arr_airport[index]



class AirplanesClasses:
    airplane = []
    rot = []

    def __init__(self, classes_list):
        for c in classes_list:
            self.airplane.append(c[0])
            self.rot.append(c[1])

    def get_rot(self, plane):
        index = self.airplane.index(plane)
        return self.rot[index]


class Airports:
    airports = []
    opening_time = []
    closing_time = []

    def __init__(self, airport_list):
        for airport in airport_list:
            self.airports.append(airport[1])
            self.opening_time.append(airport[2])
            self.closing_time.append(airport[3])

    def get_opening_time(self,airport):
        index = self.airports.index(airport)
        return self.opening_time[index]

    def get_closing_time(self,airport):
        index = self.airports.index(airport)
        return self.closing_time[index]


class ASARProblem(Problem):

    def __init__(self, filename):
        #self.initial =  # place here the initial state (or None)
        fh = open(filename)
        [A, P, L, C] = self.load(fh)
        self.airClasses = AirplanesClasses(C)
        self.airports = Airports(A)
        self.legs = Legs(L)

        self.state.airplanes_type = [i[2] for i in P]
        self.state.legs_left = P
        self.state.airplanes_last_leg =
        self.state.airplanes_time =
        #self.state = 0;

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






    """puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))
    sol = astar_search(puzzle)
    print("parent ", sol.parent, "state ", sol.state, "action ", sol.action, "path cost ", sol.path_cost, "depth ", sol.depth)
    print("grandpa", sol.parent.parent)"""


