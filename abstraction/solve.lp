% abstracted_graph atoms: center(I). center_edge(C1,C2). group(C,V).

abstracted_graph.

#program start_goal(s,g).

start(s).
goal(g).

start_group(C,L) :- start(S), group(C,S,L).
start_group(C,L+1) :- start_group(C1,L), group(C,C1,L+1).

goal_group(C,L) :- goal(G), group(C,G,L).
goal_group(C,L+1) :- goal_group(C1,L), group(C,C1,L+1).

merge_at(C,L) :- start(S), goal(G), group(C,G,L),group(C,S,L).
merge_at(C,L+1) :- goal_group(CG,L), start_group(CS,L), group(C,CG,L+1), group(C,CS,L+1), CG!=CS.
groups_before_merge(CS,CG,L) :- goal_group(CG,L), start_group(CS,L), group(C,CG,L+1), group(C,CS,L+1), CG!=CS.

#external grid.
#external abstraction.

#show.
% #show start(S) : start(S), not grid, not abstraction.
% #show goal(G) : goal(G), not grid, not abstraction.
% #show groups_before_merge(CS,CG,L) : groups_before_merge(CS,CG,L), not grid, not abstraction.
#show merge_at(C,L) : merge_at(C,L), not grid, not abstraction.

