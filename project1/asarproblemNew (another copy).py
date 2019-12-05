#!/usr/bin/env python3.6

LOCATION = 0
TIME = 1
LEGS = 2

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
        print(self.profits)
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

    def get_max_profit(self):
        inverse = [(value, key) for key, value in self.profits.items()]
        return max(inverse)[0]

    def get_id(self):
        return self.id


class Airplane:

    def __init__(self, plane, id):
        self.id = id
        self.name = plane[1]
        self.c = plane[2]

    def get_class(self):
        return self.c

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


class ASARProblem(Problem):

    def __init__(self, filename):
        #self.initial =  # place here the initial state (or None)
        fh = open(filename)
        [A, P, L, C] = self.load(fh)

        self.airClasses = {C[i][1] : C[i][2] for i in range(len(C))}

        self.airports = {A[i][1]: (A[i][2], A[i][3]) for i in range(len(A))}    # verificar closing>opening???

        self.legs = [Legs(L[i], i) for i in range(0, len(L))]
        self.planes = [Airplane(P[i], i) for i in range(0, len(P))]

        self.n_planes = len(self.planes)

        needed_info = [[-1 for p in range(len(P))], [0 for p in range(len(P))], [() for i in range(len(P))]]
        initial = (tuple([l.get_id() for l in self.legs]), tuple(tuple(i) for i in needed_info))
        #initial = state([l.get_id() for l in self.legs], [p.get_location() for p in planes])

        Problem.__init__(self, initial)

    def actions(self, state):
        # possible actions consist of applying a leg to a given plane
        possible_actions = [[p, l] for p in range(len(self.planes)) for l in state[0]]

        state_list = [list(state[0]), [list(state[1][0]), list(state[1][1]), [list(state[1][2][i]) for i in range(len(state[1][2]))]]]

        for action in possible_actions:
            # pode-se otimizar fazendo pre-processamento
            p = action[0]
            l = action[1]
            s = len(state_list[1][LEGS][p])

            if s == 0:
                pass
            # tem de começar onde o avião está
            else:
                last_leg = int(state_list[1][LEGS][p][s-1])
                #print("   last leg: ", last_leg, "\n")
                if self.legs[last_leg].get_arr_airport() != self.legs[l].get_dep_airport():
                    possible_actions.remove(action)
                    continue
            #if s!= 0:
            #    print(" matched ", self.legs[last_leg].get_arr_airport(), self.legs[l].get_dep_airport(), "\n")
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
            #print(self.airports[apt])
            if state_list[1][TIME][p] > self.airports[apt][1]:
                possible_actions.remove(action)
                continue

            #chega a uma hora em que o arrival airport ainda não fechou
            apt = self.legs[action[1]].get_arr_airport()
            if state[1][1][p] + self.legs[action[1]].get_dur() > self.airports[apt][1]:
                possible_actions.remove(action)
                continue

        return possible_actions

    def result(self, state, action):
        #print(self.airClasses)
        new_state = [list(state[0]), [list(state[1][0]), list(state[1][1]), [list(state[1][2][i]) for i in range(len(state[1][2]))]]]
        new_state[0].remove(action[1])
        p = action[0]
        l = action[1]
        new_state[1][0][p] = self.legs[l].get_arr_airport()
        dep = self.legs[l].get_dep_airport()
        arr = self.legs[l].get_arr_airport()
        leg_dur = self.legs[l].get_dur()
        classe = self.planes[p].get_class()
        new_state[1][1][p] = max(new_state[1][1][p] + leg_dur, self.airports[dep][0] + leg_dur, self.airports[arr][0])
        new_state[1][1][p] = new_state[1][1][p] + self.airClasses[classe]
        new_state[1][TIME][p] = new_state[1][TIME][p] + self.airClasses[classe]
        new_state[1][LEGS][p].append(l)

        return tuple(new_state[0]), (tuple(new_state[1][0]), tuple(new_state[1][1]), (tuple(new_state[1][2][i]) for i in range(len(new_state[1][2])) ))

    def goal_test(self, state):
        #percorreu todas as legs?
        print(state)
        if state[0] != ():
            return False
        for l in state[1][LEGS]:
            s = len(l)

            if s == 0:
                continue
            else:
                first = self.legs[l[0]].get_dep_airport()
                last = self.legs[l[s-1]].get_arr_airport()
                #print(" initial and final leg: ",l[0], l[s-1])
                if first != last:
                    return False
        return True

    def path_cost(self, c, state1, action, state2):                         # path cost g(n)
        profit = self.legs[action[1]].get_profit(self.planes[action[0]].get_class())
        # print("profi: ", profit, "leg ", action[1], "plane", self.planes[action[0]].get_class(), "\n")
        return c + 1/profit

    def h(self, node):                                              # heuristic function h(n)
        # note: use node.state to access the state
        h = 0

        """state = node.state

        legs = list(state[1][2])

        state_list = [list(state[0]), [list(state[1][0]), list(state[1][1]), [legs[i] for i in range(len(legs))]]]"""

        for leg in node.state[0]:
            h = h + 1 / self.legs[leg].get_max_profit()
            print(leg, self.legs[leg].get_max_profit())

        """for leg in state_list[0]:
            h = h + 1/self.legs[leg].get_max_profit()
            print(leg, self.legs[leg].get_max_profit())"""

        # print("  heuristica",h)

        return h

    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        lines = fh.readlines()
        return process(lines)



    def save(self, fh, state):
        i = 0
        profit = 0
        for legs_list in state[1][LEGS]:
            line = "S " + self.planes[i].get_name() + " "
            for l in legs_list:
                line = line + " " + self.legs[l].get_dep_airport() + " " + self.legs[l].get_arr_airport()
                c = self.planes[i].get_class()
                profit = profit + self.legs[l].get_profit(c)
            line = line + "\n"
            fh.write(line)
            i = i +1
        line = "P " + str(profit)
        fh.write(line)



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
        fh = open("solution.txt", "w+")
        prob = ASARProblem(sys.argv[1])
        node = astar_search(prob)
        prob.save(fh, node.state)
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()






""" puzzle = EightPuzzle((1, 2, 3, 4, 5, 6, 0, 7, 8))
    sol = astar_search(puzzle)
    print("parent ", sol.parent, "state ", sol.state, "action ", sol.action, "path cost ", sol.path_cost, "depth ", sol.depth)
    print("grandpa", sol.parent.parent)"""


