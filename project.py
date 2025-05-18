import random
import sys
from typing import Dict

shown_full_help_once = False
treasure_guardian_spawned = False


def main():
    """Main game function"""
    global treasure_guardian_spawned

    print_intro()
    player = initialize_player()
    game_world = initialize_world()

    # Track movement history {room: direction_came_from}
    movement_history = {}

    while True:
        current_room = game_world[player["location"]]
        describe_room(current_room)

        # Handle treasure room events
        if current_room["description"].startswith("An artifact glows"):
            if "armor plates" not in player["inventory"]:
                print("\nAs you step toward the artifact, deadly darts shoot from the walls!")
                print("You're pierced by dozens of poisoned projectiles!")
                player["health"] = 0
                print("\nYour vision fades as you collapse to the ground...")
                print("GAME OVER")
                print("\nTIP: Try finding armor plates before entering the treasure room!")
                break
            elif not treasure_guardian_spawned and current_room["enemy"] is None:
                # Spawn all guardians when first entering with armor
                current_room["enemies"] = ["poisonous serpent",
                                           "cursed guardian", "magical dart trap"]
                current_room["enemy"] = current_room["enemies"].pop(0)
                treasure_guardian_spawned = True
                print(
                    f"\nA {current_room['enemy']} emerges from the shadows to protect the artifact!")

        if check_victory(player, current_room):
            break

        command = get_player_input()
        process_command(command, player, game_world, movement_history)

        if check_defeat(player):
            break


def print_intro():
    """Print game introduction"""
    print("""
    DUNGEON OF THE LOST ARTIFACT
    ----------------------------
    Legend speaks of a powerful artifact hidden deep within these ruins.
    Many have entered seeking its power - none have returned.

    Can you survive the dungeon's dangers and claim the artifact?
    """)


def initialize_player() -> Dict:
    """Create player dictionary with initial stats"""
    return {
        "location": "entrance",
        "inventory": [],
        "health": 100,
        "attack": random.randint(5, 15)
    }


def initialize_world() -> Dict:
    """Create game world with rooms and connections"""
    return {
        "entrance": {
            "description": "You stand in the crumbling entrance hall. Dusty tapestries line the walls.",
            "exits": {"north": "hallway", "east": "armory"},
            "items": ["torch"],
            "enemy": None
        },
        "hallway": {
            "description": "A long hallway stretches before you. Strange markings cover the walls.",
            "exits": {"south": "entrance", "west": "library", "east": "chamber", "north": "treasure_room"},
            "items": [],
            "enemy": "giant rat"
        },
        "chamber": {
            "description": "A dark chamber filled with ancient relics. The air smells of decay.",
            "exits": {"west": "hallway", "north": "armory_back", "east": "alchemy_lab"},
            "items": ["rusty key"],
            "enemy": None
        },
        "armory": {
            "description": "An old armory with broken weapons racks.",
            "exits": {"west": "entrance", "north": "guard_room"},
            "items": ["dagger"],
            "enemy": None
        },
        "guard_room": {
            "description": "A room with rusted weapons and armor stands. A skeleton sits in the corner.",
            "exits": {"south": "armory", "east": "secret_passage"},
            "items": [],
            "enemy": "skeletal warrior"
        },
        "secret_passage": {
            "description": "A narrow, dark passageway with cobwebs covering the walls.",
            "exits": {"west": "guard_room", "east": "hidden_vault"},
            "items": ["health potion"],
            "enemy": None
        },
        "hidden_vault": {
            "description": "A small vault with an ancient chest in the center.",
            "exits": {"west": "secret_passage"},
            "items": ["gold coins"],
            "enemy": None
        },
        "armory_back": {
            "description": "The armory's back storage room. The air is thick with dust.",
            "exits": {"south": "chamber"},
            "items": ["armor plates"],
            "enemy": None
        },
        "alchemy_lab": {
            "description": "A room filled with bubbling potions and strange instruments.",
            "exits": {"west": "chamber", "north": "garden"},
            "items": ["mysterious vial"],
            "enemy": "mad alchemist"
        },
        "garden": {
            "description": "An underground garden with glowing mushrooms and strange plants.",
            "exits": {"south": "alchemy_lab"},
            "items": ["glowing mushroom"],
            "enemy": "venomous vine"
        },
        "library": {
            "description": "A ruined library with moldy books scattered everywhere.",
            "exits": {"east": "hallway", "down": "catacombs"},
            "items": ["scroll"],
            "enemy": "cursed librarian"
        },
        "catacombs": {
            "description": "Dark, damp catacombs with bones lining the walls.",
            "exits": {"up": "library", "north": "ossuary"},
            "items": ["bone charm"],
            "enemy": "ghostly apparition"
        },
        "ossuary": {
            "description": "A chamber filled with neatly stacked bones and skulls.",
            "exits": {"south": "catacombs"},
            "items": ["ancient skull"],
            "enemy": None
        },
        "treasure_room": {
            "description": "An artifact glows with an eerie light atop a stone pedestal!",
            "exits": {"south": "hallway"},
            "items": ["lost artifact"],
            "enemy": None
        }
    }


def describe_room(room: Dict):
    """Print room description and contents"""
    if (not room["description"].startswith("An artifact glows") or
            not getattr(describe_room, 'treasure_shown', False)):
        print("\n" + room["description"])

        if room["description"].startswith("An artifact glows"):
            describe_room.treasure_shown = True

    if room["items"]:
        print("You see:", ", ".join(room["items"]))

    if room["enemy"]:
        print(f"\nA {room['enemy']} blocks your path!")


def get_player_input() -> str:
    """Get and return player command"""
    return input("\nWhat will you do? ").strip().lower()


def display_tip():
    """Display a short tip or full help on first invalid input"""
    global shown_full_help_once
    print("\nI don't understand that command.")
    print("TIP: You can always check available commands by typing 'help' or '/h'.")

    if not shown_full_help_once:
        print("""
Available commands:
    - go [direction] or just [direction]: Move in a direction (north, south, east, west, up, down).
    - take [item]: Pick up an item in the current room.
    - attack or attack [enemy]: Attack the enemy in the room.
    - inventory, inv, i: Show your current inventory.
    - health, h, status: Show your current health.
    - run: Attempt to flee or act silly.
    - help, help?, /h: Show this help menu.
    - quit or /q: Exit the game.
        """)
        shown_full_help_once = True


def process_command(command: str, player: Dict, world: Dict, movement_history: Dict):
    """Process player commands and update game state"""
    current_room = world[player["location"]]

    if command in ["north", "south", "east", "west", "up", "down"]:
        handle_movement(command, player, world, movement_history)
    elif command.startswith("go "):
        direction = command[3:]
        handle_movement(direction, player, world, movement_history)
    elif command.startswith("take "):
        item = command[5:]
        take_item(item, player, current_room)
    elif command in ["inventory", "inv", "i"]:
        show_inventory(player)
    elif command in ["health", "h", "status"]:
        show_health(player)
    elif command == "attack" or command.startswith("attack "):
        if current_room["enemy"]:
            combat(player, current_room)
        else:
            print("You swing at the air, hitting nothing but your own pride.")
    elif command == "run":
        print("Your instincts scream at you to flee, but courage must prevail!")
    elif command in ["help", "help?", "/h"]:
        print("""
Available commands:
    - go [direction] or just [direction]: Move in a direction (north, south, east, west, up, down).
    - take [item]: Pick up an item in the current room.
    - attack or attack [enemy]: Attack the enemy in the room.
    - inventory, inv, i: Show your current inventory.
    - health, h, status: Show your current health.
    - run: Attempt to flee or act silly.
    - help, help?, /h: Show this help menu.
    - quit or /q: Exit the game.
        """)
    elif command in ["quit", "/q"]:
        print("The dungeon's shadows seem to grow longer as you turn away...")
        sys.exit()
    else:
        display_tip()


def handle_movement(direction: str, player: Dict, world: Dict, movement_history: Dict):
    """Handle movement with enemy attack consequences"""
    current_room = world[player["location"]]
    came_from = movement_history.get(player["location"])

    # Special case - must defeat rat to go north from hallway
    if (player["location"] == "hallway" and direction == "north" and
            current_room["enemy"] is not None):
        print("\nThe giant rat stands firm before the northern passage!")
        print("Its beady eyes gleam with malice - you must defeat it to pass!")
        return

    # Check if trying to retreat the way they came
    is_retreat = (direction == came_from if came_from else False)

    if current_room["enemy"]:
        # Calculate damage (reduced if player has armor)
        damage = random.randint(8, 18)
        if "armor plates" in player["inventory"]:
            damage = max(3, damage // 2)

        player["health"] -= damage

        if is_retreat:
            print(f"\nAs you turn to flee, the {current_room['enemy']} strikes!")
            print(f"Claws and fangs rake your back! ({damage} damage)")
            print("Cowardice has its price - next time stand your ground!")
        else:
            print(f"\nThe {current_room['enemy']} lashes out as you attempt to pass!")
            print(f"You suffer {damage} damage from the vicious attack!")
            print("TIP: Check your health with 'health' or 'h' if you feel weak.")

        if player["health"] <= 0:
            return

    # Record direction we're coming from for the next room
    if direction in current_room["exits"]:
        next_room = current_room["exits"][direction]
        movement_history[next_room] = opposite_direction(direction)

    move_player(direction, player, world)


def opposite_direction(direction: str) -> str:
    """Return opposite direction"""
    opposites = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
        "up": "down",
        "down": "up"
    }
    return opposites.get(direction, direction)


def move_player(direction: str, player: Dict, world: Dict):
    """Move player to new location if possible"""
    current_room = world[player["location"]]

    # Handle direction synonyms
    if direction == "up":
        direction = "north"
    elif direction == "down":
        direction = "south"

    if direction in current_room["exits"]:
        player["location"] = world[player["location"]]["exits"][direction]
        print(f"You move {direction}.")
    else:
        available_directions = list(current_room["exits"].keys())
        if len(available_directions) == 0:
            print("The walls offer no escape from this chamber!")
        elif len(available_directions) == 1:
            print(f"The way is blocked! Only {available_directions[0]} remains open.")
        else:
            directions_str = ", ".join(
                available_directions[:-1]) + " or " + available_directions[-1]
            print(f"Your path is barred! You can go {directions_str}.")


def take_item(item: str, player: Dict, room: Dict):
    """Add item to player inventory if present"""
    if room.get("enemy"):
        damage = random.randint(5, 12)
        if "armor plates" in player["inventory"]:
            damage = max(2, damage // 2)

        player["health"] -= damage
        print(f"\nThe {room['enemy']} strikes as you reach for the {item}!")
        print(f"A sharp pain shoots through you! ({damage} damage)")
        print("You must defeat all guardians first!")

        if player["health"] <= 0:
            return

        return

    found_item = None
    for room_item in room["items"]:
        if item == room_item or item in room_item:
            found_item = room_item
            break

    if found_item:
        player["inventory"].append(found_item)
        room["items"].remove(found_item)
        print(f"You carefully take the {found_item}.")
    else:
        print(f"No {item} lies within your grasp.")


def show_inventory(player: Dict):
    """Display player's inventory"""
    if player["inventory"]:
        print("\nYour possessions:")
        for item in player["inventory"]:
            print(f"- {item.capitalize()}")
    else:
        print("\nYour pockets hang empty and forlorn.")


def show_health(player: Dict):
    """Display player's health"""
    status = "Barely standing" if player["health"] < 25 else \
             "Wounded but steady" if player["health"] < 60 else \
             "Bruised but strong" if player["health"] < 90 else \
             "In fighting form"

    print(f"\n{status} (Health: {player['health']})")
    if player["health"] < 30:
        print("The light grows dim... find healing soon!")


def combat(player: Dict, room: Dict):
    """Handle combat with enemy"""
    enemy = room["enemy"]
    enemy_health = random.randint(25, 45)

    print(f"\nYou square off against the {enemy}!")

    while True:
        # Player attacks
        damage = player["attack"] + random.randint(3, 12)
        enemy_health -= damage
        print(f"Your strike lands true! The {enemy} reels from {damage} damage.")

        if enemy_health <= 0:
            print(f"\nWith a final blow, the {enemy} collapses!")
            print("Victory is yours... for now.")

            # Spawn next enemy if there are more
            if "enemies" in room and room["enemies"]:
                room["enemy"] = room["enemies"].pop(0)
                print(f"\nFrom the shadows, a {room['enemy']} appears to challenge you!")
            else:
                room["enemy"] = None
            break

        # Enemy attacks
        enemy_damage = random.randint(8, 16)
        if "armor plates" in player["inventory"]:
            enemy_damage = max(3, enemy_damage // 2)
        player["health"] -= enemy_damage
        print(f"The {enemy} retaliates! You suffer {enemy_damage} damage.")

        if player["health"] <= 0:
            break


def check_victory(player: Dict, room: Dict) -> bool:
    """Check if player has won the game"""
    if "lost artifact" in player["inventory"]:
        print("\nThe artifact's power surges through you!")
        print("Darkness flees before your triumph as you escape the dungeon!")
        print("VICTORY IS YOURS!")
        return True
    return False


def check_defeat(player: Dict) -> bool:
    """Check if player has lost the game"""
    if player["health"] <= 0:
        print("\nYour legs buckle as the world spins...")
        print("The cold stone greets your falling body.")
        print("As darkness takes you, one thought remains:")
        print("You have joined the dungeon's countless victims...")
        return True
    return False


if __name__ == "__main__":
    main()
