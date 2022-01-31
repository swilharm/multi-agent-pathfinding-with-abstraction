import random

class Node:
    id = 1
    def __init__(self, x, y):
        self.id = Node.id
        Node.id += 1
        self.x = x
        self.y = y
    def __str__(self):
        return f"init(object(node,{self.id}),value(at,({self.x},{self.y})))."
    def __repr__(self):
        return str(self)
        
class Robot:
    id = 1
    def __init__(self, x, y):
        self.id = Robot.id
        Robot.id += 1
        self.x = x
        self.y = y
    def __str__(self):
        return f"init(object(robot,{self.id}),value(at,({self.x},{self.y})))."
    def __repr__(self):
        return str(self)
        
class Goal:
    id = 1
    def __init__(self, x, y):
        self.id = Goal.id
        Goal.id += 1
        self.x = x
        self.y = y
    def __str__(self):
        return f"""init(object(shelf,{self.id}),value(at,({self.x},{self.y}))).
init(object(product,{self.id}),value(on,({self.id},1))).
init(object(order,{self.id}),value(line,({self.id},1))).
init(object(order,{self.id}),value(pickingStation,1))."""
    def __repr__(self):
        return str(self)
        
def main():
    nodes = []
    robots = []
    goals = []
    
    full_lines = {1, 5, 11, 15}
    every_other = {2, 6, 10, 14}
    sets_of_three = {3, 7, 9, 13}
    only_border = {4, 8, 12}
    
    for y in range(1,16):
        for x in range(1,16):
            if y in full_lines:
                nodes.append(Node(x,y))
            elif y in every_other:
                if x%2==1:
                    nodes.append(Node(x,y))
            elif y in sets_of_three:
                if x%4!=0:
                    nodes.append(Node(x,y))
            elif y in only_border:
                if x==1 or x==15:
                    nodes.append(Node(x,y))
            else:
                print(y, "not in any set")
    
    random.seed(2)
    for rid in range(1,16):
        robot_node = random.choice(nodes)
        goal_node = random.choice(nodes)
        robots.append(Robot(robot_node.x, robot_node.y))
        goals.append(Goal(goal_node.x, goal_node.y))
    
    with open("circles.lp", "w") as file:
        for node in nodes:
            file.write(str(node)+"\n")
        for robot in robots:
            file.write(str(robot)+"\n")
        file.write("init(object(pickingStation,1),value(at,(0,0)))."+"\n")
        for goal in goals:
            file.write(str(goal)+"\n")
main()