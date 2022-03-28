% translate from grid(only nodes) to graph (V, E) by adding edge between connected/adjacent vertices/nodes

node(X,Y,I):- init(object(node,I),value(at,(X,Y))).
robot(X,Y,I):- init(object(robot,I),value(at,(X,Y))).
shelf(X,Y,I):- init(object(shelf,I),value(at,(X,Y))).

diff(1,0;-1,0;0,1;0,-1).
diff(1,1;1,-1;-1,1;-1,-1).

edge(I1,I2) :- node(X1,Y1,I1), node(X2,Y2,I2), diff(X2-X1,Y2-Y1).
vertex(I) :- node(_,_,I).

% start(robot index, start vertex index) ; goal(shelf index, goal vertex index)
start(SI,VI) :- robot(X,Y,SI), node(X,Y,VI). 
goal(GI,VI) :- shelf(X,Y,GI), node(X,Y,VI). 

#external abstraction.
#show.
#show node(X,Y,I) : node(X,Y,I), not abstraction.
#show edge(V1,V2) : edge(V1,V2), not abstraction.
#show vertex(V) : vertex(V), not abstraction.
#show start(SI,VI) : start(SI,VI), not abstraction.
#show goal(GI,VI) : goal(GI,VI), not abstraction.