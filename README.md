
# Dullet Dungeon

A python turn-based rpg powered by pygame.

## Context

This game was developped as per an assignment.
The rules of the assignment were as follows:

* turn based game
* there's a hero (player character) and NPCs (ennemies)
* hero and NPCs can wield weapons that inflict damages to others but also to themselves:
    * Weapon 1: 5 dmg, 1 backlash
    * Weapon 2: 5 dmg, 1 backlash
    * Weapon 3: 5 dmg, 1 backlash
* The hero can:
    * Move (1 tile at a time)
    * Attack (when they're in the same tile as an ennemy)
    * Switch weapons
    They start without a weapon
* NPCs:
    * Can attack when it's their turn
    * Get a random weapon at the beginninf of the game
* The gameboard is in 2d
    * "X" represents NPCs
    * "O" represents the hero
* Both NPCs and heroes:
    * Start with 100 HP
    * Are assigned random coordinates on the board at the beginning
    * Heal by 1HP per round

## Installation

Clone the repository, navigate to it and install with pipenv

```bash
  pipenv install
```

If pipenv is not yet installed on your machine you can get it with:

```bash
  pip3 install pipenv
```

## Settings

A number of parameters can be customized:
* The dimensions of the board
* The amount of tiles on the board
* The width of the side menu
* The number of NPCs
* The number of NPCs displayed on the menu
* The Max Health
* The color of tiles, npcs and character
* The list of weapons and their corresponding stats

## Running

Activate your virtual environment with:

```bash
  pipenv shell
```

Then launch the game with:

```bash
  python launch.py
```

## Controls

The game is controled as follows:
* arrow keys control the character
* s to switch weapons, then 1, 2, or 3 to pick a weapon
* a to attack when a weapon is wielded
* esc or x to quit
* r to reset

## Rules
The game ends when:
* Player's health reaches 0 (defeat)
* All the NPCs are vainquished (victory)

## Limitations and possible improvements
### Menu display
The menu was designed with minimum dimensions of 400*800 minimum for the menu part.
Therefore elements might overlap or be truncated with smaller dimensions.

Ideally the margins, font sizes and shapes would resize responsively according to the available space.
However since this was not an exercise in UX design it'll do.

The code of the menu could probably gain in clarity. It contains a lot of coordinates that are not defined in variables.

### Game mechanics
The mechanics of the game itself, as per the assignment make for a rather dull game:
The only weapon that can actually beat any of the enemies is the last one as it has a dmg difference of 5, 
where the other two have a damage difference of 4.

This also means that any enemy armed with the third weapon is unbeatable as they will always hit the player first and deal,
in the best of scenarios, the exact same amount of damage with each round.

There are several ways this could be improved:
* the enemies could start with varying max HPs
* the hero could have access to more powerful weapons than the enemies
* the enemies could miss their attack sometimes

The healing of the character at a rate of 1HP per round means you need to run in circles for about 90 rounds after beating
each enemy.

### Animations and delays
Currently when a player finishes their turn, if an NPC is in position to attack they will do so immediately and without delays
or animations. This means it can be hard to distinguish between teh backlash of a weapon and the damage dealt by the enemy.
And vice versa.

A possible fix would be to add delays and animations to attacks, or at least extra text to let the player know of what is
a result of their action and what is that of the enemy.

### Pygame
Using pygame for this project was probably overkill as it's only managing the display of simple shapes and key based
user inputs.
