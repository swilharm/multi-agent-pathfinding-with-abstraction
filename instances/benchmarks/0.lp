%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Grid size X: 3
%Grid size Y: 3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program base.

%init
init(object(node, 2), value(at, (2, 1))).
init(object(node, 8), value(at, (2, 3))).
init(object(node, 3), value(at, (3, 1))).
init(object(node, 6), value(at, (3, 2))).
init(object(node, 9), value(at, (3, 3))).
init(object(node, 4), value(at, (1, 2))).
init(object(node, 7), value(at, (1, 3))).
init(object(node, 1), value(at, (1, 1))).
init(object(robot,1), value(at,(1,3))).
init(object(robot,1), value(max_energy,0)).
init(object(robot,1), value(energy,0)).
init(object(shelf,1), value(at,(3,1))).
init(object(product,0),value(on,(1,1))).
init(object(order,0),value(pickingStation,0)).
init(object(order,0),value(line,(0,1))).
