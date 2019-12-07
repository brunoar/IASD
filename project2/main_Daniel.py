#!/usr/bin/env python3.6

from aimapython.probability import elimination_ask
from aimapython.probability import BayesNet
import sys


class Problem:

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network

        lines = fh.readlines()
        [R, C, S, P, M] = process(lines)

        print(R)
        print(C)
        print(S)
        print(P)
        print(M)
        T = True
        F = False
        net = BayesNet()

        for room in R[0]:
            print(room + "0")
            net.add( (room, '', 0.5) )

        for i in range(len(S)):
            a=float(S[i][2])
            b =float(S[i][3])
            net.add(((S[i][0]), (S[i][1]), {T: a, F: b}))

        #Ver quantos parents ha

        #Criar tabela de True and False


        for room in R[0]:
            print(room + "0")
            net.add( (room, '', 0.5)



    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        #return (room, likelihood)
        pass


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

    return [R, C, S, P, M]


def main():

    if len(sys.argv) > 1:
        fh = open(sys.argv[1])
        prob = Problem(fh)
        answer = prob.solve()
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()