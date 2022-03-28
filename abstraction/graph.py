import os, pickle
from clingo.control import Control
from clingo.symbol import Number

class Graph():

    def __init__(self, name, level = 0, vertices=[]):
        self.name = name
        self.level = level
        self.vertices = set(vertices)
        self.edges = set()
        self.positions = dict()
        self.parent_vertices = dict()
        self.child_vertices = dict()
        self.starts = set()
        self.goals = set()
        self.optimality_proven = False
        # assuming there's no disjoint graphs like in N006.lp (1 means one connected graph, 2 means 2 connected subgraphs are disjoint from each other)
        self.disjoint_subgraphs = 1
        
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
    
    def add_edge(self, a, b):
        self.vertices.add(a)
        self.vertices.add(b)
        if not (b,a) in self.edges:
            self.edges.add((a,b))

    def set_position(self, vertex, x, y):
        self.positions[vertex] = (x,y)
        
    def set_parent(self, vertex, parent):
        self.parent_vertices[vertex] = parent
        
    def add_child(self, vertex, child):
        if vertex not in self.child_vertices:
            self.child_vertices[vertex] = set()
        self.child_vertices[vertex].add(child)
        
    def add_start(self, robot, vertex):
        self.starts.add((robot, vertex))
        
    def add_goal(self, goal, vertex):
        self.goals.add((goal, vertex))
        
    def clear(self):
        self.vertices.clear()
        self.edges.clear()
        self.parent_vertices.clear()
        self.child_vertices.clear()
        self.starts.clear()
        self.goals.clear()
        
    def get_subgraph(self, vertices, start_vertices, goal_vertices):
        subgraph = Graph(vertices)
        for edge in self.edges:
            if edge[0] in vertices and edge[1] in vertices:
                subgraph.add_edge(edge[0], edge[1])
        for start in self.starts:
            if start[1] in start_vertices:
                subgraph.add_start(start[0], start[1])
        for goal in self.goals:
            if goal[1] in goal_vertices:
                subgraph.add_goal(goal[0], goal[1])
        subgraph.positions = self.positions
        return subgraph
        
    def to_asp(self, add_nodes=False):
        asp = ""
        if add_nodes:
            for vertex, position in self.positions.items():
                asp += f"node({position[0]},{position[1]},{vertex}). "
        for vertex in self.vertices:
            asp += f"vertex({vertex}). "
        for edge in self.edges:
            edge_list = list(edge)
            asp += f"edge({edge_list[0]},{edge_list[1]}). "
            asp += f"edge({edge_list[1]},{edge_list[0]}). "
        for start in self.starts:
            asp += f"start({start[0]},{start[1]}). "
        for goal in self.goals:
            asp += f"goal({goal[0]},{goal[1]}). "
        return asp
        
    def safe(self, path="graphs/", cache=False):
        with open(path+self.name+'_'+str(self.level)+'.lp', 'w') as file:
            file.write(self.to_asp(add_nodes=True).replace(' ', '\n'))
        if cache:
            with open(path+'/'+self.name+'_'+str(self.level)+'.pickle', 'wb') as file:
                pickle.dump(self,file)
        
    def to_dot(self):
        dot = "strict graph {\n"
        maxY = max(self.positions.values(), key=lambda p: p[1])[1]
        for vertex, position in self.positions.items():
            dot += str(vertex)
            if vertex in self.vertices:
                dot += f' [pos="{position[0]},{maxY-position[1]}!"]'
                #dot += f' style="filled",'
                #dot += f' fillcolor="red"]'
            else:
                dot += f' [pos="{position[0]},{maxY-position[1]}!",'
                dot += f' color="lightgray",'
                dot += f' fontcolor="lightgray"]'
            dot += ";\n"
        for edge in self.edges:
            edge_list = list(edge)
            dot += f"{edge_list[0]} -- {edge_list[1]};\n"
        dot += "}\n"
        return dot
    
    def to_png(self, path="graphs/"):
        try:
            os.mkdir(path)
        except OSError as error:
            pass
        with open(path+"/.temp.graph", 'w') as file:
            file.write(self.to_dot())
        os.system(f"neato {path}/.temp.graph -Tpng > {path+'/'+self.name+'_'+str(self.level)}.png")
        os.remove(path+"/.temp.graph")
        
    def __str__(self):
        return self.to_asp()
        
    def __repr__(self):
        return str(self)

    @classmethod
    def build_graph_from_instance(cls, instance, name, level=0, grid=True):
        graph = Graph(name, level)
        def parse(model):
            for atom in model.symbols(atoms=True):
                if atom.match("vertex", 1):
                    graph.add_vertex(atom.arguments[0].number)
                elif atom.match("edge", 2):
                    graph.add_edge(atom.arguments[0].number, atom.arguments[1].number)
                elif atom.match("node", 3):
                    graph.set_position(atom.arguments[2].number, atom.arguments[0].number, atom.arguments[1].number)
                elif atom.match("start", 2):
                    graph.add_start(atom.arguments[0].number, atom.arguments[1].number)
                elif atom.match("goal", 2):
                    graph.add_goal(atom.arguments[0].number, atom.arguments[1].number)
        
        prg = Control(["--warn", "no-atom-undefined"])
        prg.load(instance)
        if grid:
            prg.load("grid_to_graph_8.lp")
        prg.ground([("base", [])])
        prg.solve(on_model=parse)
        return graph
        
    def parse_abstract_graph(self, model):
        self.abstract_graph = Graph(self.name, self.level+1)
        self.parent_vertices.clear()
        self.abstract_graph.optimality_proven = model.optimality_proven
        for atom in model.symbols(atoms=True):
            if atom.match("center", 1):
                self.abstract_graph.add_vertex(atom.arguments[0].number)
            elif atom.match("center_edge", 2):
                self.abstract_graph.add_edge(atom.arguments[0].number, atom.arguments[1].number)
            elif atom.match("center_start", 2):
                self.abstract_graph.add_start(atom.arguments[0].number, atom.arguments[1].number)
            elif atom.match("center_goal", 2):
                self.abstract_graph.add_goal(atom.arguments[0].number, atom.arguments[1].number)
            elif atom.match("group", 2):
                self.set_parent(atom.arguments[1].number, atom.arguments[0].number)
                self.abstract_graph.add_child(atom.arguments[0].number, atom.arguments[1].number)
            elif atom.match("disjoint", 1):
                self.disjoint_subgraphs = atom.arguments[0].number
        self.abstract_graph.positions = self.positions
        
    def abstract_graph_incremental(self, abstraction):
        centers = int(len(self.vertices)/9)
        ret = None
        while (ret is None or not ret.satisfiable):
            print("Trying to abstract with", centers, "centers")
            ctl = Control(["--warn", "no-atom-undefined", "--heuristic=Domain", "--opt-mode=optN", "1"])
            ctl.load(abstraction)
            ctl.add("graph", [], self.to_asp())
            parts = []
            parts.append(("graph", []))
            parts.append(("base", []))
            parts.append(("abstraction", [Number(centers)]))
            ctl.ground(parts)
            ret = ctl.solve(on_model=self.parse_abstract_graph)
            centers += 1
        return self.disjoint_subgraphs, self.abstract_graph
        
    def abstract_graph_optimize(self, abstraction, timeout=10):
        ctl = Control(["--warn", "no-atom-undefined", "--heuristic=Domain", "--opt-mode=optN", "1"])
        ctl.load(abstraction)
        ctl.add("graph", [], self.to_asp())
        parts = []
        parts.append(("graph", []))
        parts.append(("base", []))
        ctl.ground(parts)
        handle = ctl.solve(on_model=self.parse_abstract_graph, async_=True)
        handle.wait(timeout)
        handle.cancel()
        ret = handle.get()
        return self.disjoint_subgraphs, self.abstract_graph