# Wumpus World Game
Written in prolog.
Aim is to calculate predicates _**isWinner()**_ and _**wallInFront()**_ correctly.

### Game Rules
Each grid (except (1,1)) might contain a Wumpus that creates small in its 4 neighbor grids and can be seen from a grid.
The Wumpus becomes invisible after being seen.

agent actions:
- forward
- counterClockWise
- clockWise
- hit

agent senses:
- wumpusSmell
- wumpusSight
- bump

The agent wins the game, **isWinner**, if it kills a Wumpus by hit action when it is next to the Wumpus and facing it.

The agent learns the location of the walls after bumping. After learning the location, its **wallInFront** predicate should work correctly.

Check description for more details.
