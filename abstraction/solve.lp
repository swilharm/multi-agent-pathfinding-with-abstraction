abstraction.
#include <incmode>.

at(R,V,0) :- start(R,V).
{ assigned(R,S,G,V) : goal(G,V) } = 1 :- start(R,S).
{ assigned(R,S,G,V) : start(R,S) } = 1 :- goal(G,V).

#program step(t).
{ move(R,V1,V2,t) : edge(V1,V2) } 1 :- at(R,V1,t-1).
#heuristic move(C,V1,V2,T).[1,false]

at(R,V2,t) :- move(R,V1,V2,t).
at(R,V1,t) :- at(R,V1,t-1), not move(R,V1,_,t).

fulfilled(G,t) :- assigned(R,S,G,V), at(R,V,t).

#program conflicts(t).
:- at(R1,V,t), at(R2,V,t), R1<R2.
:- at(R1,V1,t-1), at(R1,V2,t), at(R2,V2,t-1), at(R2,V1,t), R1<R2.
:- at(R1,V1,t-1), at(R2,V2,t-1), at(R1,V3,t), at(R2,V4,t),
	node(X,Y,V1), node(X+1,Y,V2), node(X+1,Y+1,V3), node(X,Y+1,V4).
:- at(R1,V1,t-1), at(R2,V2,t-1), at(R1,V3,t), at(R2,V4,t),
	node(X,Y,V1), node(X+1,Y,V2), node(X+1,Y-1,V3), node(X,Y-1,V4).
:- at(R1,V1,t-1), at(R2,V2,t-1), at(R1,V3,t), at(R2,V4,t),
	node(X,Y,V1), node(X,Y+1,V2), node(X+1,Y+1,V3), node(X+1,Y,V4).
:- at(R1,V1,t-1), at(R2,V2,t-1), at(R1,V3,t), at(R2,V4,t),
	node(X,Y,V1), node(X,Y+1,V2), node(X-1,Y+1,V3), node(X-1,Y,V4).

#program check(t).
#external query(t).
:- goal(G,_), not fulfilled(G,t), query(t).
numMoves(N,t) :- N=#count{R,T : move(R,_,_,T)}.

#show.
#show move(R,V1,V2,T) : move(R,V1,V2,T).
%#show numMoves/2.
%#show assigned/4.
%#show fulfilled/2.

% Output for visualizer (requires instance file as well)
%#show occurs(object(robot,R), action(move,(DX,DY)), T) : move(R,V1,V2,T), init(object(node,V1),value(at,(X1,Y1))), init(object(node,V2),value(at,(X2,Y2))), DX=X2-X1, DY=Y2-Y1.