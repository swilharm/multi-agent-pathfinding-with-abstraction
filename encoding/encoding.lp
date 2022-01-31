#include "init.lp".
#include "action-move.lp".
#include "static.lp".
#include "fulfillment.lp".
#include "goal.lp".

horizon(14).
{occurs(object(robot, R), action(move, M), T) : action(move, M)} :- init(object(robot, R), _), time(T).

:- err(_,_,_).

%#minimize{T@2 : holds(object(order,_),  value(line,_), T)}.
#minimize{T@1,R : occurs(object(robot, R),_,T)}.

#show occurs/3.