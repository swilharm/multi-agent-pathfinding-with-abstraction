% abstracted_graph atoms: center(I). center_edge(C1,C2). group(C,V).
% python3 generate_abstractions_and_solve.py ../instances/snake9x9.lp grid_to_graph_8.lp radius_abstraction_on_graph.lp solve.lp

% #program num_of_agent(n).
#program start_and_goal(s,g).

% {single_start(SI,VI) : start(SI,VI) } =n.
% {single_goal(GI,VI) : goal(GI,VI) } =n.


start_group(s,0).
start_group(C,L+1):- start_group(C1,L), group(C,C1,L+1), not group(C,g,L+1).
% :- start_group(CS,LS), LS >= LM, merge_at(CM,LM).

goal_group(g,0).
goal_group(C,L+1) :- goal_group(C1,L), group(C,C1,L+1), not group(C,s,L+1).
% :- goal_group(CG,LG), LG >= LM, merge_at(CM,LM).

merge_at(C,LM)  :- goal_group(CG,LG), start_group(CS,LS), group(C,CG,LM), group(C,CS,LM), LS<=LM, LG<=LM.
merge(C1,L1):- merge_at(C1,L1), #count{L2: L2 < L1,merge_at(C2,L2), L1!=L2} = 0.


% % groups_before_merge(CS,CG,L) :- goal_group(CG,L), start_group(CS,L), group(C,CG,L+1), group(C,CS,L+1), CG!=CS.

% %%%% find path %%%%%
% center_edge(V1,V2,0) :- edge(V1,V2).
% % group(V,V,0) :- vertex(V).


% path(CS,CG,L):- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,CG,L).
% path(CS,C,L):- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).
% path(C,CG,L):- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).

% path(C1,C2,L):- path(C1,C2,L+1), start_group(C1,L), goal_group(C2,L), center_edge(C1,C2,L).

% path(C1,C,L):- path(C1,C2,L+1), start_group(C1,L), goal_group(C2,L), center_edge(C1,C,L), center_edge(C,C2,L).
% path(C,C2,L):- path(C1,C2,L+1), start_group(C1,L), goal_group(C2,L), center_edge(C1,C,L), center_edge(C,C2,L).

% %%
% % FIRST find connect between 2 groups, if there's connect between s and g, or s and G1, or G1 and g, use that
% path(,L-1) :- path(G1,G2,L), L>0, start_group(C1,L-1), goal_group(C2,L-1), 

% %%
% % path(CS,CG,L):- path(C1,C2,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,CG,L).

% % path(CS,C,L):- path(C1,C2,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).
% % path(C,CG,L):- path(C1,C2,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).

% % path(CS,C1,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,CG,L).
% % path(C1,C2,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,CG,L).
% % path(C2,CG,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,CG,L).

% % path(CS,C1,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,CG,L).
% % path(C1,C2,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,CG,L).
% % path(C2,C3,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,CG,L).
% % path(C3,CG,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,CG,L).

% % path(CS,C1,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,C4,L), center_edge(C4,CG,L).
% % path(C1,C2,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,C4,L), center_edge(C4,CG,L).
% % path(C2,C3,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,C4,L), center_edge(C4,CG,L).
% % path(C3,C4,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,C4,L), center_edge(C4,CG,L).
% % path(C4,CG,L):- path(_,_,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C1,L), center_edge(C1,C2,L), center_edge(C2,C3,L), center_edge(C3,C4,L), center_edge(C4,CG,L).


% quick_path(X,Y) :- path(X,Y,0).

#external grid.
#external abstraction.

#show.

% #show groups_before_merge(CS,CG,L) : groups_before_merge(CS,CG,L), not grid, not abstraction.
#show merge(C,L) : merge(C,L), not grid, not abstraction.

% #show merge_at(C,L) : merge_at(C,L), not grid, not abstraction.

% #show goal_level(C,g,L) : goal_level(C,g,L), not grid, not abstraction.
% #show start_level(C,s,L) : start_level(C,s,L), not grid, not abstraction.
 

% #show single_start(SI,VI) : single_start(SI,VI) , not grid, not abstraction.
% #show single_goal(GI,VI) : single_goal(GI,VI) , not grid, not abstraction.


% #show edge(V1,V2) : edge(V1,V2), not grid, not abstraction.
% #show vertex(V) : vertex(V), not grid, not abstraction.
% #show start_group(V,L) : start_group(V,L), not grid, not abstraction.
% #show goal_group(V,L) : goal_group(V,L), not grid, not abstraction.

% #show path(V1,V2,L) : path(V1,V2,L), not grid, not abstraction.
% #show quick_path(V1,V2) : quick_path(V1,V2), not grid, not abstraction.
% #show center_edge(CS,CG,L) : center_edge(CS,CG,L), not grid, not abstraction.

