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
            if y==8 and x!=8:
                nodes.append(Node(x,y))
            elif x==8 and y!=8:
                nodes.append(Node(x,y))
            else:
                if y==1 or y==15:
                    nodes.append(Node(x,y))
                elif x==1 or x==15:
                    nodes.append(Node(x,y))
                if y==3 or y==13:
                    if x>2 and x<14:
                        nodes.append(Node(x,y))
                elif y>3 and y<13:
                    if x==3 or x==13:
                        nodes.append(Node(x,y))
                if y==5 or y==11:
                    if x>4 and x<12:
                        nodes.append(Node(x,y))
                elif y>5 and y<11:
                    if x==5 or x==11:
                        nodes.append(Node(x,y))
                if y==7 or y==9:
                    if x>6 and x<10:
                        nodes.append(Node(x,y))
                elif y>7 and y<9:
                    if x==7 or x==9:
                        nodes.append(Node(x,y))
                        
    robots.append(Robot(1,1))
    robots.append(Robot(15,1))
    robots.append(Robot(15,15))
    robots.append(Robot(1,15))
    robots.append(Robot(3,3))
    robots.append(Robot(13,3))
    robots.append(Robot(3,13))
    robots.append(Robot(13,13))
    robots.append(Robot(7,8))
    robots.append(Robot(9,8))
                        
    goals.append(Goal(5,5))
    goals.append(Goal(5,11))
    goals.append(Goal(11,5))
    goals.append(Goal(11,11))
    goals.append(Goal(7,7))
    goals.append(Goal(7,9))
    goals.append(Goal(9,7))
    goals.append(Goal(9,9))
    goals.append(Goal(8,1))
    goals.append(Goal(8,15))
    
                        
    with open("target.lp", "w") as file:
        for node in nodes:
            file.write(str(node)+"\n")
        for robot in robots:
            file.write(str(robot)+"\n")
        file.write("init(object(pickingStation,1),value(at,(0,0)))."+"\n")
        for goal in goals:
            file.write(str(goal)+"\n")
main()