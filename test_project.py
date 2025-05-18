import pytest
import random
from project import (initialize_player, initialize_world, describe_room,
                     take_item, move_player, combat, show_inventory,
                     show_health, handle_movement)


def test_initialize_player():
    player = initialize_player()
    assert isinstance(player, dict)
    assert player["location"] == "entrance"
    assert player["inventory"] == []
    assert 5 <= player["attack"] <= 15
    assert player["health"] == 100


def test_initialize_world():
    world = initialize_world()
    assert "entrance" in world
    assert "hallway" in world
    assert "treasure_room" in world

    # Test hallway connections
    assert "north" in world["hallway"]["exits"]
    assert world["hallway"]["enemy"] == "giant rat"

    # Test treasure room properties
    assert world["treasure_room"]["items"] == ["lost artifact"]
    assert world["treasure_room"]["enemy"] is None


def test_describe_room(capsys):
    room = {
        "description": "Test room",
        "items": ["key"],
        "enemy": None
    }
    describe_room(room)
    captured = capsys.readouterr()
    assert "Test room" in captured.out
    assert "key" in captured.out

    room["enemy"] = "test monster"
    describe_room(room)
    captured = capsys.readouterr()
    assert "test monster" in captured.out


def test_take_item():
    player = {"inventory": [], "health": 100}
    room = {"items": ["torch"], "enemy": None}

    take_item("torch", player, room)
    assert "torch" in player["inventory"]
    assert "torch" not in room["items"]

    room["items"] = ["gem"]
    room["enemy"] = "guard"
    take_item("gem", player, room)
    assert "gem" not in player["inventory"]
    assert player["health"] < 100


def test_move_player():
    world = {
        "room1": {
            "exits": {"north": "room2"},
            "items": [],
            "enemy": None
        },
        "room2": {
            "exits": {"south": "room1"},
            "items": [],
            "enemy": None
        }
    }
    player = {"location": "room1", "inventory": []}

    # Test valid movement
    move_player("north", player, world)
    assert player["location"] == "room2"

    # Test invalid direction
    move_player("west", player, world)


def test_combat(capsys):
    player = {"attack": 10, "health": 100, "inventory": []}
    room = {"enemy": "test enemy", "enemies": []}

    original_randint = random.randint
    random.randint = lambda a, b: 10

    try:
        combat(player, room)
        captured = capsys.readouterr()
        assert "test enemy" in captured.out
        assert "collapses" in captured.out
        assert room["enemy"] is None
    finally:
        random.randint = original_randint


def test_handle_movement_with_enemy(capsys):
    world = {
        "room1": {
            "exits": {"north": "room2"},
            "items": [],
            "enemy": "guard"
        },
        "room2": {
            "exits": {"south": "room1"},
            "items": [],
            "enemy": None
        }
    }
    player = {"location": "room1", "inventory": [], "health": 100}

    # Test movement blocked by enemy
    handle_movement("north", player, world, {})
    captured = capsys.readouterr()
    assert "guard" in captured.out
    # Player should still move but take damage
    assert player["health"] < 100


def test_treasure_room_guardians(capsys):
    world = initialize_world()
    player = {
        "location": "treasure_room",
        "inventory": ["armor plates"],
        "health": 100,
        "attack": 15
    }
    room = {"enemy": "guardian1", "enemies": ["guardian2"]}

    combat(player, room)
    captured = capsys.readouterr()
    assert "guardian1" in captured.out
    assert room["enemy"] == "guardian2"


def test_show_inventory(capsys):
    player = {"inventory": ["sword", "potion"]}
    show_inventory(player)
    captured = capsys.readouterr()
    assert "Sword" in captured.out
    assert "Potion" in captured.out

    player = {"inventory": []}
    show_inventory(player)
    captured = capsys.readouterr()
    assert "empty" in captured.out.lower()


def test_show_health(capsys):
    player = {"health": 75}
    show_health(player)
    captured = capsys.readouterr()
    assert "75" in captured.out

    player = {"health": 20}
    show_health(player)
    captured = capsys.readouterr()
    assert "dim" in captured.out
