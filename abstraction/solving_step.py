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
        self._visited = dict()
        self._assignments = dict()
        self._plan = list()
        for atom in model.symbols(atoms=True):
            if atom.match("at", 3):
                # Take note of all vertices visited per robot
                robot = atom.arguments[0].number
                vertex = atom.arguments[1].number
                if robot not in self._visited:
                    self._visited[robot] = set()
                self._visited[robot].add(vertex)
            elif atom.match("assigned", 4):
                # Take note of goal assignments
                robot_id = atom.arguments[0].number
                start_vertex = atom.arguments[1].number
                goal_id = atom.arguments[2].number
                goal_vertex = atom.arguments[3].number
                if (start_vertex, goal_vertex) not in self._assignments:
                    self._assignments[(start_vertex, goal_vertex)] = set()
                self._assignments[(start_vertex, goal_vertex)].add((robot_id,goal_id))
            elif atom.match("move", 4):
                self._plan.append(atom)

    def solve(self, solver, graph, robotsMoving=0, is_ground_level = False, nodes = ''):
        ctl = Control(["--warn", "no-atom-undefined", "--heuristic=Domain", "--opt-mode=optN", "1"])
        ctl.load(solver)
        if is_ground_level:
            input = graph.to_asp(add_nodes=True)
            if 'node' not in input:
                input += nodes
        else:
            input = graph.to_asp()
        input += f"robotsMoving({robotsMoving}). "
        for vertices in self.assignments:
            for ids in self.assignments[vertices]:
                input += f"assigned({ids[0]},{vertices[0]},{ids[1]},{vertices[1]}). "
        ctl.add("graph", [], input)
        ctl.ground([("graph", []), ("base", [])])
        step, ret = 0, None
        # Incremental solve the subproblem
        while (ret is None or not ret.satisfiable):
            parts = []
            parts.append(("check", [Number(step)]))
            if step > 0:
                ctl.release_external(Function("query", [Number(step-1)]))
                parts.append(("step", [Number(step)]))
            ctl.ground(parts)
            if is_ground_level:
                ctl.ground([("lvl", [Number(0)])])
            ctl.assign_external(Function("query", [Number(step)]), True)
            handle = ctl.solve(on_model=self.extract_path, async_=True)
            handle.wait(1)
            handle.cancel()
            ret = handle.get()
            step = step+1
        self.solved = True
        for robot in self._visited:
            if robot in self.visited:
                self.visited[robot].update(self._visited[robot])
            else:
                self.visited[robot] = set(self._visited[robot])
        for assignment in self._assignments:
            if assignment in self.assignments:
                self.assignments[assignment].update(self._assignments[assignment])
            else:
                self.assignments[assignment] = set(self._assignments[assignment])
        self.plan.extend(self._plan)