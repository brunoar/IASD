#!/usr/bin/env python3.6

import solution
import sys


def main():
    if len(sys.argv) > 1:
        fh1 = open(sys.argv[1])
        fh2 = open("solution.txt", "w+")
        prob = solution.ASARProblem()
        prob.load(fh1)
        node = solution.search.astar_search(prob)
        if node is not None:
            prob.save(fh2, node.state)
        else:
            prob.save(fh2)
        n = node
        while(n != None):
            print(n.state)
            n = n.parent
    else:
        print("Usage: %s <filename>" % (sys.argv[0]))


main()