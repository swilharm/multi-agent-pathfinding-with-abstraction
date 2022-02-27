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
        self.abstract_level = 1
        self.output = ""
        

    def get_num_vertices(self, model):
        '''Helper function that extracts numVertices atom'''
        for atom in model.symbols(atoms=True):
            if(atom.match("numVertices", 1)):
                self.num_vertices = atom.arguments[0].number
        self.graph = ""
        for atom in model.symbols(atoms=True):
            if atom.match("vertex", 1) or atom.match("edge", 2):
                self.graph += str(atom)+'.'
    
    def extract_abstract_graph(self, model):
        self.graph = ""
        for atom in model.symbols(atoms=True):
            if atom.match("center", 1):
                self.graph += str(Function("vertex", atom.arguments))+'.'
            elif atom.match("center_edge", 2):
                self.graph += str(Function("edge", atom.arguments))+'.'
        self.print_with_periods(model)
        self.output_result(model)
    
    def print_with_periods(self, model):
        print(*(str(atom)+'.' for atom in model.symbols(shown=True)))

    def output_result(self, model):
        for atom in model.symbols(shown=True):
            self.output += str(atom)[:-1]+','+str(self.abstract_level)+'). '

    def main(self, ctl, files):
        # Ground only the instance together with rule
        # numVertices(N) :- N = #count{I : vertex(I)}.
        # to extract the number of vertices for the upper bound
        ctl = Control(["--warn", "no-atom-undefined"])
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self.get_num_vertices)
        
        while(self.num_vertices > 1):
            # Iteratively increase the number of centers and try to find a solution
            centers = int(self.num_vertices/5) # at most 5 nodes per abstracted node
            ret = None
            while (centers <= self.num_vertices and (ret is None or not ret.satisfiable)):
                print("Trying to abstract with", centers, "centers")
                ctl = Control(["--warn", "no-atom-undefined"]) 
                for f in files:
                    if not "grid_to_graph" in f:
                        if not "solve" in f:
                            ctl.load(f)
                ctl.add("graph", [], self.graph)
                ctl.ground([("base", [])])
                ctl.ground([("graph", [])])
                ctl.ground([("abstraction", [Number(centers)])])
                ret = ctl.solve(on_model=self.extract_abstract_graph)
                centers += 1
            self.num_vertices = centers-1
            self.abstract_level += 1
        
        # find path between two vertices (QuickPath approach)
        # print("Find a path from vertex ",1," to vertex ",2,":")
        print("Find the merge parent (and in which level is the merge) for vertex ",1," to vertex ",4,":")
        ctl = Control(["--warn", "no-atom-undefined"])
        for f in files:
            if not "grid_to_graph" in f:
                if not "radius_abstraction_on_graph" in f:
                    ctl.load(f)
                    
        ctl.add("abstracted_graph",[],self.output)
        ctl.ground([("base", [])])
        ctl.ground([("abstracted_graph", [])])
        # hardcoded single agent start and goal
        ctl.ground([("start_goal", [Number(1),Number(4)])])
        # get the parent that merged them
        ctl.solve(on_model=self.print_with_periods)

# Run application with commandline arguments
clingo_main(Abstraction(sys.argv[0]), sys.argv[1:])