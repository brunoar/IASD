#!/usr/bin/env python3.6

LOCATION = 0
TIME = 1
LEGS = 2
import sys
# insert at 1, 0 is the script path (or '' in REPL)
from aimapython import search

class Legs:

    def __init__(self, leg, id):
        self.id = id
        self.dep_airport = leg[1]
        self.arr_airport = leg[2]
        self.dur = hour_to_minutes(leg[3])
        self.profits = {leg[i]: leg[i + 1] for i in range(len(leg)) if i >= 4 and i % 2 == 0}

    def get_id(self):
        return self.id

    def get_dep_airport(self):
        return self.dep_airport

    def get_arr_airport(self):
        return self.arr_airport

    def get_dur(self):
        return self.dur

    def get_profit(self, c):
        return self.profits[c]

    def get_max_profit(self):
        inverse = [(value, key) for key, value in self.profits.items()]
        return max(inverse)[0]


class Airplane:

    def __init__(self, plane, id):
        self.id = id
        self.name = plane[1]
        self.c = plane[2]

    def get_name(self):
        return self.name

    def get_class(self):
        return self.c


class ASARProblem(search.Problem):

    def __init__(self):
        self.airClasses = {}
        self.airports = {}  # verificar closing>opening???
        self.legs = []
        self.planes = []
        self.number_planes = 0
        self.infeasible = 0
        self.maxprofit = 0  # Para a funcao custo e heuristica
        self.totalnodes = 0
        self.nivel_node = 0

    def actions(self, state):
        # possible actions consist of applying a leg to a given plane
        # Decomposição do estado
        (legs_left, airplanes, nivel_node) = state

        (t_available, legs) = airplanes

        (legs_done, t) = legs

        possible_actions = [[p, i] for p in range(self.number_planes) for i in legs_left]
        actions = possible_actions.copy()

        for i in range(len(actions)):
            p = actions[i][0]  # Indice aviao
            l = actions[i][1]  # Indice leg_left
            s = len(legs_done[p])

            if s != 0:
                last_leg = int(legs_done[p][s - 1])
                if self.legs[last_leg].get_arr_airport() != self.legs[l].get_dep_airport():
                    possible_actions.remove(actions[i])
                    continue

            # parte a uma hora em que o departure airport ainda não fechou
            apt = self.legs[l].get_dep_airport()
            if t_available[p] > self.airports[apt][1]:
                possible_actions.remove(actions[i])
                continue

            # chega a uma hora em que o arrival airport ainda não fechou
            apt = self.legs[l].get_arr_airport()
            if t_available[p] + self.legs[l].get_dur() > self.airports[apt][1]:
                possible_actions.remove(actions[i])
                continue

        return possible_actions

    def result(self, state, action):
        p = action[0]  # plane id
        l = action[1]  # leg id

        # Decomposição do estado em Listas
        (legs_left, airplanes, nivel_node) = state
        legs_left = list(legs_left)

        (t_available, legs) = airplanes
        t_available = list(t_available)

        (legs_done, t) = legs
        legs_done = [list(i) for i in legs_done]
        t = [list(i) for i in t]

        # Obtencao de info da leg
        dep = self.legs[l].get_dep_airport()
        arr = self.legs[l].get_arr_airport()
        leg_dur = self.legs[l].get_dur()
        classe = self.planes[p].get_class()

        #De modo a obter o numero total de nodes
        self.totalnodes += 1
        nivel_node +=1
        self.nivel_node = nivel_node

        # Atualiza tempo available do aviao
        t_available[p] = max(t_available[p] + leg_dur, self.airports[dep][0] + leg_dur, self.airports[arr][0])
        # Tempo inicio leg
        t[p].append(t_available[p] - leg_dur)
        # Somar turn around
        t_available[p] = t_available[p] + self.airClasses[classe]

        # Adicionar leg a lista de leg feitas
        legs_done[p].append(l)

        # Apagar da lista de legs por fazer
        legs_left.remove(l)

        # Conversao de novo para tuple
        legs_done = (tuple(i) for i in legs_done)
        t = (tuple(i) for i in t)

        t = tuple(t)
        legs_done = tuple(legs_done)

        legs = tuple(legs_done), tuple(t)
        t_available = tuple(t_available)

        airplanes = tuple(t_available), tuple(legs)

        legs_left = tuple(legs_left)

        new_state = tuple(legs_left), tuple(airplanes), (nivel_node)

        return new_state

    def goal_test(self, state):
        # Decomposição do estado
        (legs_left, airplanes, nivel_node) = state

        (t_available, legs) = airplanes

        (legs_done, t) = legs

        # percorreu todas as legs?
        if len(legs_left) != 0:
            return False

        for l in legs_done:
            s = len(l)
            if s == 0:
                continue
            else:
                first = self.legs[l[0]].get_dep_airport()
                last = self.legs[l[s - 1]].get_arr_airport()
                if first != last:
                    return False
        return True

    def path_cost(self, c, state1, action, state2):  # path cost g(n)
        profit = self.legs[action[1]].get_profit(self.planes[action[0]].get_class())
        return c + self.maxprofit - profit

    def heuristic(self, node):  # heuristic function h(n)
        # note: use node.state to access the state
        h = 0

        (legs_left, airplanes, nivel_node) = node.state

        for leg in legs_left:
            h = h + self.maxprofit - self.legs[leg].get_max_profit()

        if node == None:
            self.infeasible = 1
        return h

    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        lines = fh.readlines()
        [A, P, L, C] = self.process(lines)

        self.airClasses = {C[i][1]: hour_to_minutes(C[i][2]) for i in range(len(C))}
        self.airports = {A[i][1]: (hour_to_minutes(A[i][2]), hour_to_minutes(A[i][3])) for i in
                         range(len(A))}  # verificar closing>opening???
        self.legs = [Legs(L[i], i) for i in range(0, len(L))]
        self.planes = [Airplane(P[i], i) for i in range(0, len(P))]
        self.number_planes = len(P)

        legs_left = tuple([l.get_id() for l in self.legs])
        legs = tuple(() for i in enumerate(P)), tuple(() for i in enumerate(P))
        airplanes = tuple(0 for i in enumerate(P)), tuple(legs)
        nivel_node = 0
        initial = tuple(legs_left), tuple(airplanes), (nivel_node)

        for leg in legs_left:
            if self.maxprofit < self.legs[leg].get_max_profit():
                self.maxprofit = self.legs[leg].get_max_profit()
        self.maxprofit += 1

        print("Max Profit = ", self.maxprofit)
        search.Problem.__init__(self, initial)

    def save(self, fh, state=None):
        if self.infeasible == 1 or state == None:
            fh.write("Infeasible")
            return -1
        # Decomposição do estado
        (legs_left, airplanes, nivel_node) = state

        (t_available, legs) = airplanes

        (legs_done, t) = legs

        profit = 0
        for i in range(self.number_planes):
            line = "S " + self.planes[i].get_name() + " "
            if len(legs_done[i]) < 1:
                continue
            j = 0
            for l in legs_done[i]:
                if minutes_to_hour(t[i][j]) < 1000:
                    line = line + " " + "0" + str(minutes_to_hour(t[i][j])) + " " + self.legs[
                        l].get_dep_airport() + " " + self.legs[l].get_arr_airport()
                else:
                    line = line + " " + str(minutes_to_hour(t[i][j])) + " " + self.legs[l].get_dep_airport() + " " + \
                           self.legs[l].get_arr_airport()

                c = self.planes[i].get_class()
                profit = profit + self.legs[l].get_profit(c)
                j = j + 1
            line = line + "\n"
            fh.write(line)
        line = "P " + str(profit)
        fh.write(line)

    def process(self, lines):
        A = []
        P = []
        L = []
        C = []

        for ln in lines:
            if ln[0] == 'A':
                A.append([s for s in ln.split()])

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


def hour_to_minutes(h):
    return h % 100 + (h // 100) * 60


def minutes_to_hour(m):
    return (m // 60) * 100 + (m % 60)


def main():

    if len(sys.argv) > 1:
        fh = open("solution_b.txt", "w+")
        fh2 = open(sys.argv[1])
        prob = ASARProblem()
        prob.load(fh2)
        h=None
        node = search.astar_search(prob, prob.heuristic)
        if node is None:
            pass
        else:
            prob.save(fh, node.state)
        print("N = : ", prob.totalnodes, "d =", prob.nivel_node)
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()
