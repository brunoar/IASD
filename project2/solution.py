#!/usr/bin/env python3.6

LOCATION = 0
TIME = 1
LEGS = 2

from aimapython.probability import BayesNet
import sys


class Problem:

    def __init__(self, fh):
        pass
    # Place here your code to load problem from opened file object fh
    # and use probability.BayesNet() to create the Bayesian network

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)


def solver(input_file):
    return Problem(input_file).solve()

def main():
    pass

main()