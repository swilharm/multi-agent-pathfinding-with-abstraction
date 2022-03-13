abstraction.
#include <incmode>.

at(R,V,0) :- start(R,V).
{ assigned(R,G,V) : goal(G,V) } = 1 :- start(R,_).
{ assigned(R,G,V) : start(R,_) } = 1 :- goal(G,V).

#program step(t).
{ move(R,V1,V2,t) : edge(V1,V2) } 1 :- at(R,V1,t-1).
at(R,V2,t) :- move(R,V1,V2,t).
at(R,V1,t) :- at(R,V1,t-1), not move(R,V1,_,t).

fulfilled(G,t) :- assigned(R,G,V), at(R,V,t).
all_fulfilled(t) :- 0 = #count{G : goal(G,V), not fulfilled(G,t)}.

#program check(t).
#external query(t).
:- not all_fulfilled(t), query(t).

#show.
#show move(R,V1,V2,T) : move(R,V1,V2,T).

% Output for visualizer
%#show occurs(object(robot,R), action(move,(DX,DY)), T) : move(R,V1,V2,T), init(object(node,V1),value(at,(X1,Y1))), init(object(node,V2),value(at,(X2,Y2))), DX=X2-X1, DY=Y2-Y1.