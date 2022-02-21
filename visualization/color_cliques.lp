#script (python)
from clingo.symbol import String

colors = ["aqua","aquamarine","blue","blueviolet","brown","cadetblue","chartreuse","chocolate","coral","cornflowerblue","crimson","cyan","darkcyan","darkgoldenrod","darkgreen","darkmagenta","darkolivegreen","darkorange","darkorchid","darkred","darkslateblue","darkturquoise","darkviolet","deeppink","deepskyblue","dodgerblue","firebrick","forestgreen","fuchsia","gold","green","greenyellow","hotpink","indianred","indigo","lime","magenta","maroon","navy","olive","orange","orangered","orchid","purple","red","royalblue","saddlebrown","salmon","sandybrown","seagreen","sienna","slateblue","springgreen","steelblue","teal","tomato","turquoise","violet","yellow","yellowgreen"]
index = 0
mapping = dict()

def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
    
def color(id):
    global index
    if id not in mapping:
        mapping[id] = colors[index]
        index += 1
    return String(mapping[id])
#end.

#const g = colored.

v_graph(g).
v_attr(graph,1,colorscheme,"svg").

v_node(ID,g) :- init(object(node,ID),_), group(_,ID).
v_attr(node,ID,pos,@pos(X,15-Y)):- init(object(node,ID),value(at,(X,Y))), group(_,ID).
v_attr(node,ID,style,"filled"):- init(object(node,ID),_), group(_,ID).
v_attr(node,ID,fillcolor,@color(C)) :- group(C,ID).
v_attr(node,ID,penwidth,"5.0") :- center(ID).

v_edge((A,B),g) :- edge(A,B).

#show.
#show v_graph/1.
#show v_node/2.
#show v_edge/2.
#show v_attr/4.