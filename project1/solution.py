### Template ###

import search

class ASARProblem(search.Problem):

    def __init__(self):
        self.initial = # place here the initial state (or None)
    
    def actions(self, state):
        pass

    def result(self, state, action):
        pass
        
    def goal_test(self, state):
        pass
        
    def path_cost(self, c, state1, action, state2):
        pass
        
    def heuristic(self, node):
        # note: use node.state to access the state
        pass
        
    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        pass
    
    def save(self, fh, state):
        # note: fh is an opened file object
        pass
