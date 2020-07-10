# Labyrinth

* Implement the "Labyrinth" game (aka "Terra Incognita").
  - [Labyrinth (Wiki)](https://en.wikipedia.org/wiki/Labyrinth_(paper-and-pencil_game))
  - [Terra Incognita](https://www.thegamecrafter.com/games/terra-incognita)
* You should use the knowledge obtained during the course.
* Design the game using:
  - Interfaces (OOP-like)
  - Inversion of Control
  - Dependency Injection
  - Proper layering
  - Proper project structure
  - Diagrams of classes and interaction between classes
* The code should be extensible enough to support new upcoming requirements (see "Mandatory set of rules" and "Extended set of rules").

### Functional requirements

* _"Labyrinth"_ is a one-player turn-by-turn game which should be implemented as a console application.
  - Game consists of labyrinth, labyrinth objects, user inventory, CLI interface.
  - Computer is a master of game.
  - Game is controlled by text commands.
  - Initially, the player can't see the labyrinth. The player should explore the labyrinth on its own.
* User commands:
  - Starting a new game with a predefined labyrinth size: "start <labyrinth_size>". Labyrinth size should be not less 4 and not bigger 10.
  - Quiting the current game: "quit" (without saving).
  - Quiting the current game with saving: "save <file_name>" (the game should be saved into a text file).
* On the start, labyrinth should be randomly generated.
  - Labyrinth consists of **cells**.
  - A wall can be built between any two neighbour cells.
  - An outside wall is called monolith.
  - **There should be no inaccessible cells**.
  - **There should be one exit** randomly dislocated in the monolith wall.

##### Mandatory set of rules

* Game flow:
  - Player's goal to find a treasure and leave the labyrinth.
  - Games starts after the labyrinth is generated.
  - On the start, player is invited to enter commands.
  - Game prints the results of processing the commands.
  - Game ends when the player leaves the labyrinth with a treasure.
  - If the player doesn't have a treasure found, the game should say he can't leave the labyrinth on attempt to pass through the exit.
* Game objects:
  - **Treasure**.
  - **5 wormholes**, organized into a cyclic ordered set. Entering a wormhole moves the player into the next wormhole by index. Skipping a move while staying on the wormhole moves the player to the next wormhole.
* User commands:
  - **Moving**: "go up", "go down", "go left", "go right".
  - **Skipping a turn**: "skip".
* Game messages:
  - "step impossible, **wall**"
  - "step executed, **wormhole**"
  - "step executed, **treasure**"
  - "step impossible, **monolith**"
  - "step executed" (**on successful moving**)

##### Extended set of rules

* Game objects:
  - **River**. Has source and end. Several cells arranged in a chain which cannot intersect itself.
    Entering a river moves the player 2 cells down a stream (maximum).
    Skipping a turn triggers this moving again.
    River and wormholes cannot share the same cell.
  - **Bear**. Bear is like a player but moves randomly and is NPC.
    River and wormholes affect bear as well.
    Once bear and player step on the same cell, player becomes damaged.
    When damaged, the player should be also moved 1 cell away from the bear towards any passable direction.
    (If this is not possible, player stays where he was)
    Damaging the player second time makes him dead.
  - **Map**. When the player has a map he can use the "map" command to see the whole labyrinth
    (including treasure, bear, river, wormholes).
    Using this command behaves like skipping a turn (all the effects should be applied.)