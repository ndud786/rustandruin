# Rust and Ruin

A 2D top-down action-survival game built from scratch in Python with Pygame. Fight through four escalating rounds of enemies, dodge and counter with a light/heavy combat system, and race the clock for a spot on the local high score board.

![Python](https://img.shields.io/badge/python-3.x-blue) ![Pygame](https://img.shields.io/badge/pygame-2.x-green)

## Gameplay


## Features

- **Real-time combat** — separate light and heavy attacks, each with their own damage, cooldown, and hit animation
- **Dodge roll** — briefly makes the player invulnerable, timed against enemy attacks
- **Wave-based rounds** — four rounds per level with increasing enemy count and spawn rate, ending in a boss fight
- **Five enemy types**, each with unique sprites, health, and speed
- **Tile-based level** built from a Tiled map editor export (separate tile, item, and collision layers)
- **Persistent high scores** — top 5 fastest level-clear times saved locally and shown on their own screen
- **Full menu flow** — start screen, controls reference, and high scores screen, with animated fade transitions between states

## Controls

| Input | Action |
|---|---|
| `W` `A` `S` `D` | Move |
| `Q` | Dodge roll |
| Left click | Light attack |
| Right click | Heavy attack |

## Tech stack

- Python 3
- [Pygame](https://www.pygame.org/)
- Levels designed in [Tiled](https://www.mapeditor.org/), exported as CSV layers

## Getting started

```bash
git clone <your-repo-url>
cd rust-and-ruin

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python main.py
```

## Project structure

```
main.py          # game loop, menus, asset loading
characters.py    # Character/Enemy classes — movement, combat, animation
levels.py        # Level class — round progression, spawning, HUD
sprites.py       # Map and spritesheet helper classes
constants.py     # screen dimensions
highscores.txt   # persisted top-5 completion times
files/           # sprites, tilesets, and level CSVs (see Credits)
```

## Known limitations

This was my first full project, built while I was still learning. A few things I'd do differently now:

- `main.py` currently handles menus, asset loading, and the game loop together — I'd split these into separate scene/state classes
- Some naming conventions and magic numbers (animation frame thresholds, spawn timings) aren't as clean as I'd like in hindsight
- No automated tests yet
- Only one level is implemented, though the round/enemy system is built to support more

## Credits

Character/enemy/tile art sourced from free asset packs; original creators not identified — happy to add proper credit if you recognize these