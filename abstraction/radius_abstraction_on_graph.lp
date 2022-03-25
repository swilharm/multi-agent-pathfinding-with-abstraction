% clingo radius_abstraction_on_graph.lp snake9x9graph3.lp 0

abstraction.
numVertices(N) :- N = #count{I : vertex(I)}.
% radius(1).

%% un-/comment these to run it with/without python
%#const n = 17.
#program abstraction(n).

{center(I): vertex(I)} = n.

group(C,C) :- center(C).
group(C,V) :- center(C), vertex(V), edge(C,V), n==1.
{ group(C,V) }:- center(C), vertex(V), edge(C,V), n>1, not group(C1,V), C1 != C, center(C1). 

% vertex cannot have 0 group or more than 1 group
:- vertex(V), not group(_,V).
:- vertex(V), #count{C: group(C,V)} > 1.

% edge
center_edge(C1,C2) :- group(C1,V1), vertex(V1), edge(V1,V2), group(C2,V2), vertex(V2), C1!=C2, V1!=V2.
center_edge(C1,C2) :- center_edge(C2,C1).

% start and goal
center_start(R,C) :- start(R,V), group(C,V).
center_goal(G,C) :- goal(G,V), group(C,V).

% dectect the number of disjoint subgraphs (when none of center has any edge between them)
disjoint(C) :- C = #count{ I : center(I) }, C > 1, not center_edge(_,_).

#external grid.
#show.
#show center_edge(C1,C2) : center_edge(C1,C2), not grid.
#show center(I) : center(I), not grid.
#show group(C,V) : group(C,V), not grid.
#show disjoint(C) : disjoint(C), not grid.
% Alternative output that can be fed into the next iteration
%#show vertex(V) : center(V), not grid.
%#show edge(V1,V2) : center_edge(V1,V2), not grid.

% Output for clingraph
#show init(object(node,I),value(at,(X,Y))) : init(object(node,I),value(at,(X,Y))), clingraph.
#show center_edge(C1,C2) : center_edge(C1,C2), clingraph.
#show center(I) : center(I), clingraph.
#show group(C,V) : group(C,V), clingraph.
#show center_start(R,V) : center_start(R,V), clingraph.
#show center_goal(G,V) : center_goal(G,V), clingraph.
#show vertex(V) : vertex(V), clingraph.
#show edge(V1,V2) : edge(V1,V2), clingraph.
#show start(R,V) : start(R,V), clingraph.
#show goal(G,V) : goal(G,V), clingraph.