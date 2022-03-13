#script (python)
from clingo.symbol import String

def pos(x,y):
    return String(f"{str(x)},{str(y)}!")

def label(id, type, value):
    if type.match("start",0):
        return String(f"S{value}")
    else:
        return String(f"G{value}")

#end.

#const g = display.

maxY(MY) :- init(object(node,_),value(at,(_,MY))), MY=#max{Y : init(object(node,ID),value(at,(X,Y)))}.

v_graph(g).

v_node(ID,g) :- init(object(node,ID),value(at,(X,Y))).
v_attr(node,ID,pos,@pos(X,MY-Y)):- init(object(node,ID),value(at,(X,Y))), maxY(MY).
v_attr(node,ID,xlabel,@label(ID, start, S)) :- v_node(ID,g), start(S,ID).
v_attr(node,ID,xlabel,@label(ID, goal, G)) :- v_node(ID,g), goal(G,ID).
v_attr(node,ID,fontcolor,"lightgray") :- v_node(ID,g), not vertex(ID).
v_attr(node,ID,color,"lightgray") :- v_node(ID,g), not vertex(ID).

v_edge((A,B),g) :- edge(A,B).

#show.
#show v_graph/1.
#show v_node/2.
#show v_edge/2.
#show v_attr/4.