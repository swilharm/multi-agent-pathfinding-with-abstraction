%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Grid size X: 4
%Grid size Y: 5
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program base.

%init
init(object(node, 2), value(at, (2, 1))).
init(object(node, 10), value(at, (2, 3))).
init(object(node, 3), value(at, (3, 1))).
init(object(node, 11), value(at, (3, 3))).
init(object(node, 5), value(at, (1, 2))).
init(object(node, 9), value(at, (1, 3))).
init(object(node, 1), value(at, (1, 1))).
init(object(node, 4), value(at, (4, 1))).
init(object(node, 8), value(at, (4, 2))).
init(object(node, 12), value(at, (4, 3))).
init(object(node, 16), value(at, (4, 4))).
init(object(node, 20), value(at, (4, 5))).
init(object(node, 13), value(at, (1, 4))).
init(object(node, 17), value(at, (1, 5))).
init(object(node, 18), value(at, (2, 5))).
init(object(node, 19), value(at, (3, 5))).
init(object(robot,1), value(at,(1,5))).
init(object(robot,1), value(max_energy,0)).
init(object(robot,1), value(energy,0)).
init(object(shelf,1), value(at,(4,1))).
init(object(product,0),value(on,(1,1))).
init(object(order,0),value(pickingStation,0)).
init(object(order,0),value(line,(0,1))).
