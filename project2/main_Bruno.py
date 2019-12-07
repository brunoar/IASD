#!/usr/bin/env python3.6

from aimapython.probability import elimination_ask
from aimapython.probability import BayesNet
import sys


class Problem:

    def __init__(self, fh):
        lines = fh.readlines()
        [self.R, self.C, self.S, self.P, self.M] = process(lines)
        """"print(self.R)
        print(self.C)
        print(self.S)
        print(self.P)
        print(self.M)"""""
        parentsR = []
        parentsS = []
        for room in self.R:                         # dictionary that associates each room with it adjacent rooms
            parents = []
            for edge in self.C:
                if edge[0] == room:
                    parents.append(edge[1])           # confirm that this isn't a problem
                elif edge[1] == room:
                    parents.append(edge[0])
            parentsR.append(parents)
            parents = []
            for sensor in self.S:
                if sensor[1] == room:               # allows more than one sensor per room
                    parents.append(sensor[0])
            parentsS.append(parents)
        self.adjDict = {self.R[i]: parentsR[i] for i in range(len(self.R))}
        self.sensDict = {self.R[i]: parentsS[i] for i in range(len(self.R))}
        self.prob = {r : 0.5 for r in self.R}
        print(self.adjDict)
        print(self.sensDict)

    def solve(self):
        # sample time 0
        node_specs = []
        i = 0
        for room in self.R:
            print(room)
            X = room + str(i)
            node_specs.append((X, '', 0.5))

        T,F = True, False
        #as many sample times as given in the file
        for sample in self.M:
            i = i + 1
            node_specs = []
            cpt = {}
            for room in self.R:
                parents = ''
                X = room + str(i)
                for p in self.adjDict[room]:
                    parents = parents + ' ' + p + str(i-1)
                    #place probability cpt
                    
                for s in self.sensDict[room]:
                    parents = parents + ' ' + s + str(i)
                    #place probability cpt
                node_specs.append((X, parents, cpt))
        """"net = BayesNet(node_specs) 
        a = self.R[1]+'0'
        b = {self.R[0]+'0':True}
        p = elimination_ask(a, b, net).show_approx()
        print(p)"""""
        # return (room, likelihood)


def process(lines):
    R=[]
    C=[]
    S=[]
    P=[]
    M=[]

    for ln in lines:

            if ln[0] == 'R':
                R.append([s for s in ln.split()[1:] ])

            if ln[0] == 'C':
                doors = ln.split()[1:]
                for door in doors:
                    aux = []
                    for i in range(len(door)):
                        if door[i] == ',':
                            aux.append(door[0:i])
                            aux.append(door[i+1:])
                    C.append(aux)

            if ln[0] == 'S':
                sensors = ln.split()
                for s in sensors[1:]:
                    j=0
                    aux = []
                    for i in range(len(s)):
                        if s[i] == ':':
                            aux.append(s[j:i])
                            j=i+1
                    aux.append(s[j:-1])
                    S.append(aux)

            if ln[0] == 'P':
                P.append([s for s in ln.split()[1:] ])

            if ln[0] == 'M':
                measures = ln.split()[1:]
                sampling = []
                for m in measures:
                    aux = []
                    for i in range(len(m)):
                        if m[i] == ':':
                            aux.append(m[0:i])
                            aux.append(m[i+1:])
                    sampling.append(aux)
                M.append(sampling)

    #return [R[0], C[0], S[0], P[0], M[0]]                   # melhorar isto
    return [R[0], C, S, P, M]

def main():

    if len(sys.argv) > 1:
        fh = open(sys.argv[1])
        prob = Problem(fh)
        answer = prob.solve()
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()