import sys, os, argparse, time
from typing import Optional
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.solving import SolveResult
from clingo.symbol import Function, Number

class Abstraction(Application):
    def __init__(self, name):
        self.program_name = name
        self.num_vertices = 0
        self.graphs = []
        self.groups = []
        self.visited = dict()
        self.goal_assignments = dict()
        self.goal_assignments[0] = 0
        self.path = []

    def get_num_vertices(self, model):
        '''Extracts numVertices atom and the initial graph'''
        self.graph = ""
        self.graphs.append(set())
        for atom in model.symbols(atoms=True):
            if(atom.match("numVertices", 1)):
                self.num_vertices = atom.arguments[0].number
            elif atom.match("vertex", 1) or atom.match("edge", 2) or atom.match("start", 2) or atom.match("goal", 2):
                self.graph += str(atom)+'. '
                self.graphs[-1].add(atom)
    
    def extract_abstract_graph(self, model):
        '''Extracts abstracted graph'''
        self.graph = ""
        self.graphs.append(set())
        self.groups.append(dict())
        for atom in model.symbols(atoms=True):
            if atom.match("center", 1):
                self.graph += str(Function("vertex", atom.arguments))+'. '
                self.graphs[-1].add(Function("vertex", atom.arguments))
            elif atom.match("center_edge", 2):
                self.graph += str(Function("edge", atom.arguments))+'. '
                self.graphs[-1].add(Function("edge", atom.arguments))
            elif atom.match("center_start", 2):
                self.graph += str(Function("start", atom.arguments))+'. '
                self.graphs[-1].add(Function("start", atom.arguments))
            elif atom.match("center_goal", 2):
                self.graph += str(Function("goal", atom.arguments))+'. '
                self.graphs[-1].add(Function("goal", atom.arguments))
            elif atom.match("group", 2):
                self.groups[-1][atom.arguments[1].number] = atom.arguments[0].number
        self.print_with_periods(model)
    
    def extract_path(self, model):
        '''Extracts path through graph'''
        for atom in model.symbols(atoms=True):
            if atom.match("at", 3):
            # Take not of all vertices visited per robot
                robot = atom.arguments[0].number
                vertex = atom.arguments[1].number
                if robot not in self.visited:
                    self.visited[robot] = set()
                self.visited[robot].add(vertex)
            elif atom.match("assigned", 3):
            # Take not of goal assignments
                robot = atom.arguments[0].number
                vertex = atom.arguments[2].number
                self.goal_assignments[robot] = vertex
        self.path.extend(model.symbols(shown=True))
    
    def print_with_periods(self, model):
        print(*(str(atom)+'.' for atom in model.symbols(shown=True)))

    def main(self, args):
        # Ground only the instance together with rule
        # numVertices(N) :- N = #count{I : vertex(I)}.
        # to extract the number of vertices for the upper bound
        start_abstract = time.time()
        ctl = Control(["--warn", "no-atom-undefined"])
        ctl.load(args.instance)
        ctl.load(args.graph)
        ctl.load(args.abstraction)
        ctl.ground([("base", [])])
        ctl.solve(on_model=self.get_num_vertices)
        
        while(self.num_vertices > 1):
            print("\nGenerating abstraction level", len(self.graphs))
            # Iteratively increase the number of centers and try to find a solution
            centers = int(self.num_vertices/5) # at most 5 nodes per abstracted node
            ret = None
            while (centers <= self.num_vertices and (ret is None or not ret.satisfiable)):
                print("Trying to abstract with", centers, "centers")
                ctl = Control(["--warn", "no-atom-undefined"])
                ctl.load(args.abstraction)
                ctl.load(args.instance)
                ctl.add("graph", [], self.graph)
                ctl.ground([("base", [])])
                ctl.ground([("graph", [])])
                ctl.ground([("abstraction", [Number(centers)])])
                ret = ctl.solve(on_model=self.extract_abstract_graph)
                centers += 1
            self.num_vertices = centers-1
        end_abstract = time.time()
            
        #SOLVE
        start_solve = time.time()
        for level in range(len(self.graphs)-1, -1, -1):
            print("\nFinding paths on abstraction level", level)
            goals = set(self.goal_assignments.values())
            # Split planning into goal vertices and plan robots together that are moving to the same vertex
            for goal_vertex in goals:
                ctl = Control(["--warn", "no-atom-undefined"])
                ctl.load(args.solver)
                if level == len(self.graphs)-1:
                    # At maximum abstraction, load full graph
                    # Bit of a dirty trick by adding a zero assignment just so this loop is entered on the highest level
                    self.goal_assignments.pop(0)
                    graph = ''.join(str(atom)+'.' for atom in self.graphs[level])
                else:
                    # Determine all robots with the selected goal vertex
                    robots = set(item[0] for item in self.goal_assignments.items() if item[1]==goal_vertex)
                    graph_atoms = set()
                    for atom in self.graphs[level]:
                        # Assemble graph only with the vertices and edges that were visited by these robots on the higher abstraction
                        if atom.match("vertex", 1):
                            for robot in robots:
                                if self.groups[level][atom.arguments[0].number] in self.visited[robot]:
                                    graph_atoms.add(str(atom))
                        elif atom.match("edge", 2):
                            for robot in robots:
                                if self.groups[level][atom.arguments[0].number] in self.visited[robot] and self.groups[level][atom.arguments[1].number] in self.visited[robot]:
                                    graph_atoms.add(str(atom))
                        elif atom.match("start", 2):
                            if atom.arguments[0].number in robots:
                                graph_atoms.add(str(atom))
                        elif atom.match("goal", 2):
                            if self.groups[level][atom.arguments[1].number] == goal_vertex:
                                graph_atoms.add(str(atom))
                    graph = '. '.join(graph_atoms)+'.'
                ctl.add("graph", [], graph)
                step, ret = 0, None
                # Incremental solve the subproblem
                while (ret is None or not ret.satisfiable):
                    parts = []
                    parts.append(("check", [Number(step)]))
                    if step > 0:
                        ctl.release_external(Function("query", [Number(step-1)]))
                        parts.append(("step", [Number(step)]))
                    else:
                        parts.append(("graph", []))
                        parts.append(("base", []))
                    ctl.ground(parts)
                    ctl.assign_external(Function("query", [Number(step)]), True)
                    ret, step = ctl.solve(on_model=self.extract_path), step+1
            # Print out combined paths
            print(*(str(atom)+'.' for atom in self.path))
            self.path = []
        end_solve = time.time()
        
        print(f"Abstraction: {end_abstract-start_abstract:.3f}s, Solving: {end_solve-start_solve:.3f}s, Total: {end_solve-start_abstract:.3f}s")

def parse():
    '''Reads the program arguments as flagged parameters'''
    parser = argparse.ArgumentParser(
        description="Abstraction solver for asprilo instances"
    )
    parser.add_argument('--graph', '-g', metavar='<file>',
                        help='Encoding turning grid instance into graph with vertices and edges', required=True)
    parser.add_argument('--abstraction', '-a', metavar='<file>',
                        help='Encoding abstracting the map', required=True)
    parser.add_argument('--solver', '-s', metavar='<file>',
                        help='Encoding solving on a graph', required=True)
    parser.add_argument('--instance', '-i', metavar='<file>',
                        help='Map instance', required=True)
    args = parser.parse_args()
    if not os.path.isfile(args.graph):
        raise IOError("file %s not found!" % args.graph)
    if not os.path.isfile(args.abstraction):
        raise IOError("file %s not found!" % args.abstraction)
    if not os.path.isfile(args.solver):
        raise IOError("file %s not found!" % args.solver)
    if not os.path.isfile(args.instance):
        raise IOError("file %s not found!" % args.instance)
    return args

# Run application with commandline arguments
Abstraction(sys.argv[0]).main(parse())