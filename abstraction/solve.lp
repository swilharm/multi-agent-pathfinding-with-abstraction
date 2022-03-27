abstraction.
#include <incmode>.

% Neeeded when running solve.lp on its own
%robotsMoving(N) :- N= #count{R:start(R,_)}.

at(R,V,0) :- start(R,V).
{chosen(R,S) : start(R,S)} = N :- robotsMoving(N).
{ assigned(R,S,G,V) : goal(G,V) } = 1 :- chosen(R,S).
:- goal(G,_), assigned(R1,_,G,_), assigned(R2,_,G,_), R1<R2.
:- start(R,_), assigned(R,_,G1,_), assigned(R,_,G2,_), G1<G2.

#program step(t).
{ move(R,V1,V2,t) : edge(V1,V2) } 1 :- chosen(R,_), at(R,V1,t-1).
#heuristic move(C,V1,V2,T).[1,false]
#minimize{1,T,R: move(R,_,_,T)}.

at(R,V2,t) :- move(R,V1,V2,t).
at(R,V1,t) :- at(R,V1,t-1), not move(R,V1,_,t).

% conflict only applies to original graph at level 0 (no abstraction) 
#program lvl(l).
level(l).
% vertex conflict
:- at(R1,V,T), at(R2,V,T), R1<R2, level(0). 
% edge conflict
:- at(R1,V1,T-1), at(R1,V2,T), at(R2,V2,T-1), at(R2,V1,T), R1<R2, level(0).
% path crossing conflict
:- at(R1,V1,T-1), at(R2,V2,T-1), at(R1,V3,T), at(R2,V4,T),
	node(X,Y,V1), node(X+1,Y,V2), node(X+1,Y+1,V3), node(X,Y+1,V4), level(0).
:- at(R1,V1,T-1), at(R2,V2,T-1), at(R1,V3,T), at(R2,V4,T),
	node(X,Y,V1), node(X+1,Y,V2), node(X+1,Y-1,V3), node(X,Y-1,V4), level(0).
:- at(R1,V1,T-1), at(R2,V2,T-1), at(R1,V3,T), at(R2,V4,T),
	node(X,Y,V1), node(X,Y+1,V2), node(X+1,Y+1,V3), node(X+1,Y,V4), level(0).
:- at(R1,V1,T-1), at(R2,V2,T-1), at(R1,V3,T), at(R2,V4,T),
	node(X,Y,V1), node(X,Y+1,V2), node(X-1,Y+1,V3), node(X-1,Y,V4), level(0).

#program check(t).
#external query(t).
:- goal(G,V), start(R,S), assigned(R,S,G,V), not at(R,V,t), query(t).

#show.
#show move/4.
%#show assigned/4.

% Output for visualizer (requires instance file as well)
%#show occurs(object(robot,R), action(move,(DX,DY)), T) : move(R,V1,V2,T), init(object(node,V1),value(at,(X1,Y1))), init(object(node,V2),value(at,(X2,Y2))), DX=X2-X1, DY=Y2-Y1.