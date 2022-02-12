% translate from grid(only nodes) to graph (V, E) by adding edge between connected/adjacent vertices/nodes

node(X,Y,I):- init(object(node,I),value(at,(X,Y))).
diff(1,0;-1,0;0,1;0,-1).

edge(I1,I2) :- node(X1,Y1,I1), node(X2,Y2,I2), diff(X2-X1,Y2-Y1).
vertex(I) :- node(_,_,I).

#external abstraction.
#show.
#show edge(V1,V2) : edge(V1,V2), not abstraction.
#show vertex(V) : vertex(V), not abstraction.
