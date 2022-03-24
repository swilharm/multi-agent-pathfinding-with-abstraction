from clingo.control import Control
from clingo.symbol import Number, Function

class SolvingStep():
    
    def __init__(self, level):
        self.level = level
        self.assignments = dict()
        self.visited = dict()
        self.plan = list()
        self.solved = False
    
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
                robot_id = atom.arguments[0].number
                start_vertex = atom.arguments[1].number
                goal_id = atom.arguments[2].number
                goal_vertex = atom.arguments[3].number
                if (start_vertex, goal_vertex) not in self.assignments:
                    self.assignments[(start_vertex, goal_vertex)] = []
                self.assignments[(start_vertex, goal_vertex)].append((robot_id, goal_id))
            elif atom.match("move", 4):
                self.plan.append(atom)
                
    def solve(self, solver, graph):
        ctl = Control(["--warn", "no-atom-undefined"])
        ctl.load(solver)
        ctl.add("graph", [], graph.to_asp())
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
        self.solved = True