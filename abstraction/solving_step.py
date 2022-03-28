from clingo.control import Control
from clingo.symbol import Number, Function

class SolvingStep():
    
    def __init__(self, level):
        self.level = level
        self.assignments = dict()
        self.visited = dict()
        self.at = list()
        self.plan = list()
        self.asprilo = ""
        self.unsat = False
        
        self._visited = dict()
        self._assignments = dict()
        self._at = list()
        self._plan = list()
    
    def extract_path(self, model):
        '''Extracts path through graph'''
        self._visited = dict()
        self._assignments = dict()
        self._at = list()
        self._plan = list()
        for atom in model.symbols(atoms=True):
            if atom.match("at", 3):
                # Take note of all vertices visited per robot
                robot = atom.arguments[0].number
                vertex = atom.arguments[1].number
                if robot not in self._visited:
                    self._visited[robot] = set()
                self._visited[robot].add(vertex)
                self._at.append(atom)
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
        self.asprilo = ''.join(str(atom)+'. ' for atom in model.symbols(shown=True))


    def solve_incremental(self, solver, graph, robotsMoving=0, maxtime=1, is_ground_level = False):
        ctl = Control(["--warn", "no-atom-undefined", "--heuristic=Domain", "--opt-mode=optN", "1"])
        ctl.load(solver)
        input = graph.to_asp(add_nodes=is_ground_level)
        input += f"robotsMoving({robotsMoving}). "
        for vertices in self.assignments:
            for ids in self.assignments[vertices]:
                input += f"assigned({ids[0]},{vertices[0]},{ids[1]},{vertices[1]}). "
        for at in self.at:
            input += str(at)+'. '
        #print(input)
        ctl.add("graph", [], input)
        ctl.ground([("base", []), ("graph", [])])
        step, ret = 0, None
        # Incremental solve the subproblem
        while step<=maxtime and (ret is None or not ret.satisfiable):
            parts = []
            parts.append(("check", [Number(step)]))
            if step > 0:
                ctl.release_external(Function("query", [Number(step-1)]))
                parts.append(("step", [Number(step)]))
                if is_ground_level:
                    parts.append(("conflicts", [Number(step)]))
            ctl.ground(parts)
            ctl.assign_external(Function("query", [Number(step)]), True)
            handle = ctl.solve(on_model=self.extract_path, async_=True)
            handle.wait(5)
            handle.cancel()
            ret = handle.get()
            step = step+1
        if step > maxtime:
            print(f"Could not find solution in {maxtime} steps")
            self.unsat = True
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
        self.at.extend(self._at)
                
    def solve_optimize(self, solver, graph, robotsMoving, maxtime, timeout=5):
        ctl = Control(["--warn", "no-atom-undefined", "--heuristic=Domain", "--opt-mode=optN", "1"])
        ctl.load(solver)
        input = graph.to_asp()
        for vertices in self.assignments:
            for ids in self.assignments[vertices]:
                input += f"assigned({ids[0]},{vertices[0]},{ids[1]},{vertices[1]}). "
        input += f"robotsMoving({robotsMoving}). "
        input += f"maxtime({maxtime}). "
        ctl.add("graph", [], input)
        ctl.ground([("graph", []), ("base", [])])
        handle = ctl.solve(on_model=self.extract_path, async_=True)
        handle.wait(timeout)
        handle.cancel()
        ret = handle.get()
        print(ret)
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
        self.at.extend(self._at)