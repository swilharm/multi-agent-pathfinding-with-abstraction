#program start_and_goal(s,s_index,g,g_index).

% tracing start vertex's merging process (from level 0 to highest)
start_group(s,0).
start_group(C,L+1):- start_group(C1,L), group(C,C1,L+1), not group(C,g,L+1).
% tracing goal vertex's merging process
goal_group(g,0).
goal_group(C,L+1) :- goal_group(C1,L), group(C,C1,L+1), not group(C,s,L+1).

%%%%%%%%%% get the level and center the two vertices merged %%%%%%%%%%
merge_at(C,LM)  :- goal_group(CG,LG), start_group(CS,LS), group(C,CG,LM), group(C,CS,LM), LS<=LM, LG<=LM.
merge(C1,L1):- merge_at(C1,L1), #count{L2: L2 < L1,merge_at(C2,L2), L1!=L2} = 0.

%%%%%%%%%%%%%%%%%%%%%%%%%% find path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
center_edge(V1,V2,0) :- edge(V1,V2).

% path between 2 groups before merging: 1. (  S) - (G ) ; 2. S - C - G
{ visit(CS,CG,L)}:- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,CG,L).
{ visit(CS,C,L)}:- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).
{ visit(C,CG,L)}:- merge(C,L+1), start_group(CS,L), goal_group(CG,L), center_edge(CS,C,L), center_edge(C,CG,L).

% % 1. IF start and goal groups are adjacent: S - G
{ visit(C1,C2,L-1) }:- visit(G1,G2,L), L>0, start_group(C1,L-1), goal_group(C2,L-1), center_edge(C1,C2,L-1). 

{ visit(C1,C3,L-1) }:- visit(G1,G2,L), L>0, start_group(C1,L-1), goal_group(C2,L-1), not center_edge(C1,C2,L-1), group(G2,C3,L), center_edge(C1,C3,L-1). 
{ visit(C3,C2,L-1) }:- visit(G1,G2,L), L>0, start_group(C1,L-1), goal_group(C2,L-1), not center_edge(C1,C2,L-1), group(G1,C3,L), center_edge(C3,C2,L-1). 

{ visit(C3,C4,L-1) }:- visit(G1,G2,L), L>0, start_group(C1,L-1), goal_group(C2,L-1), not center_edge(C1,C2,L-1), group(G2,C4,L), not center_edge(C1,C4,L-1), group(G1,C3,L), not center_edge(C3,C2,L-1), center_edge(C3,C4,L-1). 

{ visit(C1,C3,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L), start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), center_edge(C1,C3,L), not_same(C1,C2,C3), not_same(C2,C3,C4).
{ visit(C4,C2,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L),start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), center_edge(C4,C2,L), not_same(C1,C2,C3), not_same(C2,C3,C4).

{ visit(C1,CS,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L),start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), not center_edge(C1,C3,L), not_same(C1,C2,C3), not_same(C2,C3,C4).
{ visit(CS,C3,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L),start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), not center_edge(C1,C3,L), not_same(C1,C2,C3), not_same(C2,C3,C4).

{ visit(C4,CG,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L),start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), not center_edge(C4,C2,L), not_same(C1,C2,C3), not_same(C2,C3,C4).
{ visit(CG,C2,L) }:- visit(C3,C4,L), start_group(C1,L), goal_group(C2,L),start_group(CS,L+1), goal_group(CG,L+1), group(CS,C3,L+1), group(CG,C4,L+1), not center_edge(C4,C2,L), not_same(C1,C2,C3), not_same(C2,C3,C4).

% bridge path points in non start/goal groups
{ visit(C3,C4,L)}:- visit(_,C3,L), visit(C4,_,L), not in_sg(C3,L+1), not in_gg(C4,L+1), center_edge(C3,C4,L).
{ visit(C3,C5,L)}:- visit(_,C3,L), visit(C4,_,L), not in_sg(C3,L+1), not in_gg(C4,L+1), not center_edge(C3,C4,L), center_edge(C3,C5,L), center_edge(C5,C4,L), not_same(C5,C3,C4).
{ visit(C5,C4,L)}:- visit(_,C3,L), visit(C4,_,L), not in_sg(C3,L+1), not in_gg(C4,L+1), not center_edge(C3,C4,L), center_edge(C3,C5,L), center_edge(C5,C4,L), not_same(C5,C3,C4).

% bridge path points in start/goal groups 3)],[(4, but no 6)[(7 8 9)
{ visit(C1,C3,L) }:- visit(C3,_,L), in_sg(C3,L+1), start_group(C1,L), center_edge(C1,C3,L).
{ visit(C1,C4,L) }:- visit(C3,_,L), in_sg(C3,L+1), start_group(C1,L), same_g(C1,C4,L+1), not center_edge(C1,C3,L), center_edge(C1,C4,L), center_edge(C4,C3,L), not_same(C1,C3,C4).
{ visit(C4,C3,L) }:- visit(C3,_,L), in_sg(C3,L+1), start_group(C1,L), same_g(C1,C4,L+1), not center_edge(C1,C3,L), center_edge(C1,C4,L), center_edge(C4,C3,L), not_same(C1,C3,C4).

% visit(6,7,0), visit(8,9,0)
{ visit(C4,C2,L) }:- visit(_,C4,L), in_gg(C4,L+1), goal_group(C2,L), center_edge(C4,C2,L).
{ visit(C4,C5,L) }:- visit(_,C4,L), in_gg(C4,L+1), goal_group(C2,L), same_g(C2,C5,L+1), not center_edge(C4,C2,L), center_edge(C4,C5,L), center_edge(C5,C2,L), not_same(C2,C4,C5).
{ visit(C5,C2,L) }:- visit(_,C4,L), in_gg(C4,L+1), goal_group(C2,L), same_g(C2,C5,L+1), not center_edge(C4,C2,L), center_edge(C4,C5,L), center_edge(C5,C2,L), not_same(C2,C4,C5).

% these are generated just to make it easier to form the body
not_same(C1,C2,C3) :- C1!=C2, C2!=C3, C3!=C1, vertex(C1), vertex(C2), vertex(C3).
same_g(C1,C2,L) :- group(G,C1,L),group(G,C2,L).
in_sg(C,L) :- start_group(CG,L), group(CG,C,L).
in_gg(C,L) :- goal_group(CG,L), group(CG,C,L).

:- not visit(s,_,0).
:- not visit(_,g,0).
% no divergence
:- visit(V1,V2,0), visit(V1,V3,0), V2!=V3.
:- visit(V2,V1,0), visit(V3,V1,0), V2!=V3.
% no backwards
:- visit(V1,V2,0), visit(V2,V1,0), V2!=V1.
% if a path can be skipped, skip it
:- visit(V1,V2,0), visit(V2,V3,0), center_edge(V1,V3,0). 
% no breaks
:- visit(V1,_,0), not visit(_,V1,0), V1!=s.
:- visit(_,V2,0), not visit(V2,_,0), V2!=g.

% get path steps (could later be used to synchronise with other agents' paths)
path_len(T) :- T = #count{ (V1,V2): visit(V1,V2,0)}.
path(s_index,s,C2,1) :- visit(s,C2,0).
path(s_index,C2,C3,T+1) :- visit(C2,C3,0), path(_,C1,C2,T), T<=L, path_len(L).
:- path(_,_,g,T), T != L, path_len(L).
:- not path(_,_,g,_).

#external grid.
#external abstraction.

#show.
#show path(SI,C1,C2,T) : path(SI,C1,C2,T), not grid, not abstraction.