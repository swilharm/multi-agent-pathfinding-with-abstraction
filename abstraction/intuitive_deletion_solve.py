from graph import Graph
import sys, os, argparse, time
from typing import Optional
from clingo.application import Application, clingo_main
from clingo.control import Control
from clingo.solving import SolveResult
from clingo.symbol import Function, Number

class Abstraction(Application):
    def __init__(self):
        self.graphs = []
        self.groups = []
        self.visited = dict()
        self.assignments = dict()
        self.assignments[0] = (0,0,0,0)
        self.path = []
    
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
            elif atom.match("assigned", 4):
                # Take note of goal assignments
                self.assignments[atom.arguments[0].number] = (atom.arguments[0].number, atom.arguments[1].number, atom.arguments[2].number, atom.arguments[3].number)
        self.path.extend(model.symbols(shown=True))
    
    def print_with_periods(self, model):
        print(*(str(atom)+'.' for atom in model.symbols(shown=True)))

    def main(self, args):
        start_abstract = time.time()
        self.graphs.append(Graph.build_graph_from_instance(args.instance, "circles"))
        self.graphs[-1].to_png()
        i = 1
        while len(self.graphs[-1].vertices) > 1:
            print("\nGenerating abstraction level", i)
            i += 1
            self.graphs.append(self.graphs[-1].abstract_graph(args.abstraction))
            self.graphs[-1].safe()
            self.graphs[-1].to_png()
        end_abstract = time.time()
        
        #SOLVE
        start_solve = time.time()
        for level in range(len(self.graphs)-1, -1, -1):
            print("\nFinding paths on abstraction level", level)
            assignments = dict()
            for assignment in self.assignments.values():
                if (assignment[1],assignment[3]) not in assignments:
                    assignments[(assignment[1],assignment[3])] = []
                assignments[(assignment[1],assignment[3])].append(assignment)
            # Split planning into start/goal combinations and plan robots together that are moving together
            for start_goal_assignment in assignments:
                ctl = Control(["--warn", "no-atom-undefined"])
                ctl.load(args.solver)
                #ctl.load(args.instance)
                if level == len(self.graphs)-1:
                    # At maximum abstraction, load full graph
                    # Bit of a dirty trick by adding a zero assignment just so this loop is entered on the highest level
                    self.assignments.pop(0)
                    graph = self.graphs[level].to_asp()
                else:
                    # Determine all robots with the selected goal vertex
                    robots = [assignment[0] for assignment in assignments[start_goal_assignment]]
                    goals = [assignment[2] for assignment in assignments[start_goal_assignment]]
                    visited = set()
                    for robot in robots:
                        for vertex in self.visited[robot]:
                            visited.update(self.graphs[level+1].child_vertices[vertex])
                    graph = self.graphs[level].get_subgraph(list(visited), robots, goals).to_asp()
                    #print({assignment[0]: (assignment[1], assignment[3]) for assignment in assignments[start_goal_assignment]})
                    #print(graph)
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
Abstraction().main(parse())