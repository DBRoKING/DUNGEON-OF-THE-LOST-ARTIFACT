# DUNGEON OF THE LOST ARTIFACT
#### Video Demo: <https://youtu.be/A5rvkrin1UI>
#### Description:
Dungeon of the Lost Artifact is a text-based adventure game where players navigate through a dangerous dungeon to retrieve a powerful magical artifact. The game features inventory management, combat mechanics, and multiple endings based on player choices. Written entirely in Python, this project demonstrates object-oriented programming principles, game state management, and interactive storytelling.

**Game Overview**

The player begins at the entrance of an ancient dungeon filled with many paths to explore, traps, and enemies. To win, players must explore rooms, collect essential items, defeat guardians, and ultimately claim the lost artifact. The game features:
- 14 unique rooms with interconnected paths
- 8 different enemy types with varying difficulty
- 12 collectible items including weapons, armor, and keys
- Progressive difficulty with multiple guardians in the treasure room
- Health management and combat system
- Movement tracking and directional history

**Key Features**
- **Inventory System**: Players can collect and use items like armor plates (for damage reduction), health potions, and keys to progress.
- **Combat Mechanics**: Turn-based combat where both player and enemy deal damage each turn. Armor reduces incoming damage.
- **Treasure Room Puzzle**: The final challenge requires specific items and involves defeating multiple guardians in sequence.
- **Movement History**: The game tracks which direction players came from, affecting enemy attack behavior during retreats.
- **Progressive Difficulty**: Enemies become more challenging as players approach the treasure room.

**File Structure**
- `project.py`: Main game file containing all game logic, including:
  - `main()`: Primary game loop and state manager
  - `initialize_player()`: Creates player character with stats
  - `initialize_world()`: Builds the dungeon map and room connections
  - `combat()`: Handles turn-based fighting mechanics
  - `handle_movement()`: Manages player navigation and enemy interactions
- `test_project.py`: Contains pytest unit tests for core game functions

**Implementation Details**
The game uses a dictionary-based world structure where each room contains:
- Description text
- Available exits (connections to other rooms)
- Items present in the room
- Enemies that must be defeated

Special mechanics include:
- **Armor System**: Reduces damage taken by 50% when player has armor plates
- **Treasure Guardians**: Spawn sequentially when player first enters treasure room with armor
- **Poison Dart Trap**: Instant death in treasure room without armor
- **Directional Tracking**: Enemies deal bonus damage when players retreat

**How to Play**
1. Run `project.py` using Python 3.12
2. Read room descriptions carefully for clues about items and dangers
3. Navigate using compass directions (north, south, east, west, up, down)
4. Collect items with 'take [item]' command
5. Fight enemies with 'attack' command
6. Manage health and inventory carefully
7. Find armor plates before attempting the treasure room
8. Defeat all guardians to claim the artifact and win

**Testing**
The project includes comprehensive unit tests covering:
- Player initialization
- World structure validation
- Room description functionality
- Item collection mechanics
- Combat resolution
- Movement handling
- Health display formatting
- Inventory management

Run tests with: `pytest test_project.py`

**Development Challenges**
Key challenges overcome during development:
1. Implementing sequential guardian spawning in treasure room
2. Balancing combat difficulty with armor damage reduction
3. Creating meaningful room connections that allow for exploration
4. Designing the poison dart trap as a "soft lock" to teach players about preparation
5. Implementing movement history for realistic retreat penalties

**Dependencies**
- Python 3.12
- pytest (for testing only)

No additional packages required - runs with standard library modules.

**Developer Info**
- **Created by**: Dinuga Dewdun (DBRoKING)
- **GitHub**: [DBRoKING](https://github.com/DBRoKING)
- **edX**: dinugadewdun
- **Location**: Colombo, Sri Lanka
- **Date**: April 19, 2025

**Acknowledgments**
Special thanks to CS50P for providing the foundation in Python programming that made this project possible. The text adventure format was chosen to demonstrate core programming concepts including data structures, control flow, and user input handling in a creative format.

*CS50P 2025 Final Project Submission*
