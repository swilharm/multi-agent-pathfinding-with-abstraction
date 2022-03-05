% clingo solve_multi_paths.lp

% Find the merge parent (and in which level is the merge) for  for vertex  4 (id: 1 ) to vertex  9 (id: 1 ):
path(1,4,5,1). path(1,5,6,2). path(1,6,7,3). path(1,7,8,4). path(1,8,9,5).
% Find the merge parent (and in which level is the merge) for  for vertex  9 (id: 2 ) to vertex  4 (id: 2 ):
path(2,4,5,1). path(2,5,6,2). path(2,6,7,3). path(2,7,8,4). path(2,8,9,5).
%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%% define conflicts %%%%%%%%%%%%%%%%%%%%
% 1. occupying same cell at same time
conflict(cell,I1,I2,V,T,nan) :- path(I1,_,V,T), path(I2,_,V,T), I1 != I2, I1 < I2.
% 2. using same edge (same direction/different direction)
conflict(edge,I1,I2,V1,V2,T) :- path(I1,V1,V2,T), path(I2,V1,V2,T), I1 != I2, I1 < I2.
conflict(edge,I1,I2,V1,V2,T) :- path(I1,V1,V2,T), path(I2,V2,V1,T), I1 != I2, I1 < I2.

%%%%%%%%%%%%%%%%%%%% conflict resolution %%%%%%%%%%%%%%%%%%%%

#show conflict/6.