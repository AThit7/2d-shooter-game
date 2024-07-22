# 2D Shooter Game

This game's mechanics resembles the classic GTA 1 and 2. The goal is to defeat all enemies on a map.

## Installation

1. Install the required dependencies:

```sh
pip install pygame
```

2. Clone the repository:

```sh
git clone https://github.com/AThit7/2d-shooter-game.git
```

2. Navigate to the project directory:

```sh
cd 2d-shooter-game
```

## Running the Game

To start the game, run the following command:

```sh
python main.py
```

## Map Customization

You can modify the map by editing the file located at `assets/maps/map1.map`. The map file uses a simple grid-based format with the following rules:

- `0` represents an empty space.
- `1` represents a wall.
- `2` represents the starting position.
- `3` represents an enemy spawn point.

Each number represents a tile on the map, and the map is defined in a comma-separated format. Here is a basic example:

```
1, 1, 1, 1, 1
1, 2, 0, 3, 1
1, 0, 0, 0, 1
1, 1, 1, 1, 1
```

## Controls

- **W/A/S/D**: Move up/left/down/right
- **Mouse**: Aim
- **Left Click**: Shoot

## Gameplay
https://raw.githubusercontent.com/AThit7/2d-shooter-game/main/readme-assets/gameplay.mp4
