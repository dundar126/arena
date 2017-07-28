# ARENA
By **Stephen Campbell**

## Overview
   The game takes place on a 10x10 grid. Moves are taken as turns. The goal is to lure the enemy into mines you place to deplete their health.
   The enemy will make decisions to try to win based on game conditions, including placing mines, tracking the player and healing itself.

## Strategy
**General**
- Place mines and lure the enemy into them to win.
- The game ends when either the player or the enemy reach 0 health.
- Both the player and the enemy have 100 health.

**The enemy**
- The enemy will hurt the player with 50 damage if they make contact with it unless they can make a fast escape (like jumping over a wall), in which case the player will be hurt by 25 damage.
- Enemy mines deal you 25 damage.
- The enemy will heal by up to 50 health if it is threatened. It can only do this once. The player does not get this ability.

**The player**
- The player's mines deal 25 damage to the enemy.
- The player can jump over single walls (not double walls) to get away from the enemy. The enemy does not have this ability.
- The player is limited to 6 mines, the enemy can place infinite.
- The player can only place a mine once every 3 turns at the most. The enemy does not have this limitation.
- Placing mines in the choke points (like between walls) is a good strategy for increasing the chance of the enemy hitting them.

## Controls
- Space: place mine
- Arrow keys or WASD: Move player

## AI
The following AI techniques were used in this game:
- A* pathfinding
    - Used to track the player around the walls
- Fuzzy system for enemy decision making
    - Enemy will heal if player proximity is close and enemy on low health
- Neural network for enemy decision making
    - Enemy is more likely to track the player when the player's health is low and they have few mines left
    
## Running the game
Requires numpy and pygame:
`pip3 install numpy pygame`

Run the main.py file with Python 3:
`python3 main.py`
