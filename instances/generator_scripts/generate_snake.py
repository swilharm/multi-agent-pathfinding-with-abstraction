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
    
    for y in range(1,16):
        for x in range(1,16):
            if y%2==1:
                nodes.append(Node(x,y))
            elif y%4==0:
                if x==1:
                    nodes.append(Node(x,y))
            else:
                if x==15:
                    nodes.append(Node(x,y))
                    
    robots.append(Robot(1,1))
    robots.append(Robot(2,1))
    robots.append(Robot(3,1))
    robots.append(Robot(4,1))
    robots.append(Robot(5,1))
    goals.append(Goal(1,15))
    goals.append(Goal(2,15))
    goals.append(Goal(3,15))
    goals.append(Goal(4,15))
    goals.append(Goal(5,15))
    
    with open("snake15x15.lp", "w") as file:
        for node in nodes:
            file.write(str(node)+"\n")
        for robot in robots:
            file.write(str(robot)+"\n")
        file.write("init(object(pickingStation,1),value(at,(0,0)))."+"\n")
        for goal in goals:
            file.write(str(goal)+"\n")
main()