#script (python)
from clingo.symbol import String

colors = ['darkcyan', 'orange', 'lime', 'blue', 'deeppink', 'forestgreen', 'darkblue', 'maroon3', 'red', 'yellow', 'burlywood', 'aqua', 'fuchsia', 'darkslategray', 'seagreen', 'darkred', 'olive', 'darkorange', 'mediumorchid', 'mediumspringgreen', 'darksalmon', 'dodgerblue', 'palegoldenrod', 'plum', 'lightskyblue', 'darkolivegreen', 'saddlebrown', 'olivedrab', 'slategray', 'darkslateblue', 'green', 'mediumseagreen', 'rosybrown', 'darkgoldenrod', 'steelblue', 'chocolate', 'yellowgreen', 'lightseagreen', 'indianred', 'indigo', 'limegreen', 'darkseagreen', 'darkmagenta', 'tan', 'darkorchid', 'gold', 'mediumblue', 'crimson', 'deepskyblue', 'greenyellow', 'tomato', 'orchid', 'thistle', 'khaki', 'lightgreen', 'lightblue', 'mediumslateblue', 'lightsalmon', 'aquamarine', 'hotpink', 'sienna', 'brown', 'maroon2', 'midnightblue', 'firebrick', 'cadetblue', 'lightslategray', 'rebeccapurple', 'darkkhaki', 'peru', 'goldenrod', 'purple2', 'mediumturquoise', 'mediumaquamarine', 'orangered', 'darkturquoise', 'slateblue', 'mediumvioletred', 'lawngreen', 'turquoise', 'darkviolet', 'springgreen', 'royalblue', 'sandybrown', 'lightcoral', 'lightsteelblue', 'coral', 'palevioletred', 'salmon', 'powderblue', 'skyblue', 'violet']
index = 0
mapping = dict()

def pos(x,y):
    return String(f"{str(x)},{str(y)}!")

def label(id, type, value):
    if type.match("start",0):
        return String(f"S{value}")
    else:
        return String(f"G{value}")
    
def color(id):
    global index
    if id not in mapping:
        mapping[id] = colors[index]
        index += 1
    return String(mapping[id])
#end.

#const g = colored.

maxY(MY) :- init(object(node,_),value(at,(_,MY))), MY=#max{Y : init(object(node,ID),value(at,(X,Y)))}.

v_graph(g).

v_node(ID,g) :- init(object(node,ID),value(at,(X,Y))).
v_attr(node,ID,pos,@pos(X,MY-Y)):- init(object(node,ID),value(at,(X,Y))), maxY(MY).
v_attr(node,ID,xlabel,@label(ID, start, S)) :- v_node(ID,g), start(S,ID).
v_attr(node,ID,xlabel,@label(ID, goal, G)) :- v_node(ID,g), goal(G,ID).
v_attr(node,ID,style,"filled"):- vertex(ID).
v_attr(node,ID,fillcolor,@color(C)) :- group(C,ID).
v_attr(node,ID,penwidth,"5.0") :- center(ID).
v_attr(node,ID,fontcolor,"lightgray") :- v_node(ID,g), not vertex(ID).
v_attr(node,ID,color,"lightgray") :- v_node(ID,g), not vertex(ID).

v_edge((A,B),g) :- edge(A,B).

#show.
#show v_graph/1.
#show v_node/2.
#show v_edge/2.
#show v_attr/4.
#show maxY/1.