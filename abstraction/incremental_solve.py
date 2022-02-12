import sys
from typing import Optional
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.solving import SolveResult
from clingo.symbol import Function, Number

class Abstraction(Application):
    def __init__(self, name):
        self.program_name = name
        self.num_vertices = 0
        

    def get_num_vertices(self, model):
        '''Helper function that extracts numVertices atom'''
        for atom in model.symbols(atoms=True):
            if(atom.match("numVertices", 1)):
                self.num_vertices = atom.arguments[0].number
    
    def print_with_periods(self, model):
        print(*(str(atom)+'.' for atom in model.symbols(shown=True)))

    def main(self, ctl, files):
        # Ground only the instance together with rule
        # numVertices(N) :- N = #count{I : vertex(I)}.
        # to extract the number of vertices for the upper bound
        ctl = Control(["--warn", "no-atom-undefined"])
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self.get_num_vertices)
        
        # Iteratively increase the number of centers and try to find a solution
        centers = int(self.num_vertices/5) # at most 5 nodes per abstracted node
        ret = None
        while (centers <= self.num_vertices and (ret is None or not ret.satisfiable)):
            print("Trying to abstract with", centers, "centers")
            ctl = Control(["--warn", "no-atom-undefined"])
            for f in files:
                ctl.load(f)
            ctl.ground([("base", [])])
            ctl.ground([("abstraction", [Number(centers)])])
            ret = ctl.solve(on_model=self.print_with_periods)
            centers += 1

# Run application with commandline arguments
clingo_main(Abstraction(sys.argv[0]), sys.argv[1:])