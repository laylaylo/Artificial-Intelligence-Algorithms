:- use_module(library(clpfd)).

dir(1, east). % Start facing east
loc(1, 1, 1). % Start at point (1,1)
bump(0).

loc(T1, R, C) :-
	T0 #= T1 - 1,
	_up #= R - 1,
	_down #= R + 1,
	_left #= C - 1,
	_right #= C + 1,
	(
		(action(T0, forward), dir(T0, east), loc(T0, R, _left), not(bump(T1)));
		(action(T0, forward), dir(T0, west), loc(T0, R, _right), not(bump(T1)));
		(action(T0, forward), dir(T0, south), loc(T0, _up, C), not(bump(T1)));
		(action(T0, forward), dir(T0, north), loc(T0, _down, C), not(bump(T1)));
		((action(T0, clockWise);action(T0, counterClockWise);action(T0, hit)), loc(T0, R, C));
		(action(T0, forward), bump(T1), loc(T0, R, C))
	).

dir(T1, east) :-
	T0 #= T1 - 1,
	( 
		((action(T0, forward); action(T0, hit)), dir(T0, east));
		(action(T0, clockWise), dir(T0, north));
		(action(T0, counterClockWise), dir(T0, south))
	).

dir(T1, south) :-
	T0 #= T1 - 1,
	( 
		((action(T0, forward); action(T0, hit)), dir(T0, south));
		(action(T0, clockWise), dir(T0, east));
		(action(T0, counterClockWise), dir(T0, west))
	).

dir(T1, west) :-
	T0 #= T1 - 1,
	( 
		((action(T0, forward); action(T0, hit)), dir(T0, west));
		(action(T0, clockWise), dir(T0, south));
		(action(T0, counterClockWise), dir(T0, north))
	).

dir(T1, north) :-
	T0 #= T1 - 1,
	( 
		((action(T0, forward); action(T0, hit)), dir(T0, north));
		(action(T0, clockWise), dir(T0, west));
		(action(T0, counterClockWise), dir(T0, east))
	).

isWall(R, C) :-
	_up #= R - 1,
	_down #= R + 1,
	_left #= C - 1,
	_right #= C + 1,
	(
		(loc(T0, R, _left), action(T0, forward), dir(T0, east), T1 is T0 + 1, bump(T1));
		(loc(T0, _up, C), action(T0, forward), dir(T0, south), T1 is T0 + 1, bump(T1));
		(loc(T0, R, _right), action(T0, forward), dir(T0, west), T1 is T0 + 1, bump(T1));
		(loc(T0, _down, C), action(T0, forward), dir(T0, north), T1 is T0 + 1, bump(T1))
	).

wallInFront(T1) :-
	(
		(dir(T1, east), loc(T1, R, C) -> WallR is R, WallC is C + 1);
		(dir(T1, south), loc(T1, R, C) -> WallR is R + 1, WallC is C);
		(dir(T1, west), loc(T1, R, C) -> WallR is R, WallC is C - 1);
		(dir(T1, north), loc(T1, R, C) -> WallR is R - 1, WallC is C)
	),
	isWall(WallR, WallC).

mightBeWumpusBySmell(R, C) :-
	_up #= R - 1,
	_down #= R + 1,
	_left #= C - 1,
	_right #= C + 1,
	(
		(wumpusSmell(T), loc(T, _up, C));
		(wumpusSmell(T), loc(T, _down, C));
		(wumpusSmell(T), loc(T, R, _left));
		(wumpusSmell(T), loc(T, R, _right))
	).

mightBeWumpusBySight(R, C) :-
	_up #= R - 1,
	_up_up #= R - 2,
	_up_up_up #= R - 3,
	_up_up_up_up #= R - 4,
	_down #= R + 1,
	_down_down #= R + 2,
	_down_down_down #= R + 3,
	_down_down_down_down #= R + 4,
	_left #= C - 1,
	_left_left #= C - 2,
	_left_left_left #= C - 3,
	_left_left_left_left #= C - 4,
	_right #= C + 1,
	_right_right #= C + 2,
	_right_right_right #= C + 3,
	_right_right_right_right #= C + 4,
	(
		(wumpusSight(T), dir(T, east), (loc(T, R, _left); loc(T, R, _left_left); loc(T, R, _left_left_left); loc(T, R, _left_left_left_left)));
		(wumpusSight(T), dir(T, south), (loc(T, _up, C); loc(T, _up_up, C); loc(T, _up_up_up, C); loc(T, _up_up_up_up, C)));
		(wumpusSight(T), dir(T, west), (loc(T, R, _right); loc(T, R, _right_right); loc(T, R, _right_right_right); loc(T, R, _right_right_right_right)));
		(wumpusSight(T),loc(T, X, Y), dir(T, north), (loc(T, _down, C); loc(T, _down_down, C); loc(T, _down_down_down, C); loc(T, _down_down_down_down, C)))
	).

noWumpus(R, C) :-
	(R =:= 1, C =:= 1);
	(R < 1 ; C < 1);
	loc(T, R, C).

isWinner(T1) :-
	action(T1, hit),
	loc(T1, R, C),
	(
		(dir(T1, east) -> KillR is R, KillC is C + 1, Neighbour1R is R, Neighbour1C is C - 1, Neighbour2R is R + 1, Neighbour2C is C, Neighbour3R is R - 1, Neighbour3C is C);
		(dir(T1, south)  -> KillR is R + 1, KillC is C, Neighbour1R is R, Neighbour1C is C - 1, Neighbour2R is R, Neighbour2C is C + 1, Neighbour3R is R - 1, Neighbour3C is C);
		(dir(T1, west) -> KillR is R, KillC is C - 1, Neighbour1R is R, Neighbour1C is C + 1, Neighbour2R is R + 1, Neighbour2C is C, Neighbour3R is R - 1, Neighbour3C is C);
		(dir(T1, north) -> KillR is R - 1, KillC is C, Neighbour1R is R, Neighbour1C is C - 1, Neighbour2R is R, Neighbour2C is C + 1, Neighbour3R is R + 1, Neighbour3C is C)
	),
	(not(noWumpus(KillR, KillC)), mightBeWumpusBySmell(KillR, KillC), mightBeWumpusBySight(KillR, KillC)),
	(noWumpus(Neighbour1R, Neighbour1C); not((mightBeWumpusBySmell(Neighbour1R, Neighbour1C), mightBeWumpusBySight(Neighbour1R, Neighbour1C)))),
	(noWumpus(Neighbour2R, Neighbour2C); not((mightBeWumpusBySmell(Neighbour2R, Neighbour2C), mightBeWumpusBySight(Neighbour2R, Neighbour2C)))),
	(noWumpus(Neighbour3R, Neighbour3C); not((mightBeWumpusBySmell(Neighbour3R, Neighbour3C), mightBeWumpusBySight(Neighbour3R, Neighbour3C)))).
