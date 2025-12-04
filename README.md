# Asteroids Game

A modern, feature-rich implementation of the classic Asteroids arcade game built with Python and Pygame.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

![Showcase](./docs/showcase.gif)

## Features

### Core Gameplay
- **Classic Asteroids Mechanics**: Destroy asteroids to score points and avoid collisions
- **Smooth Movement**: Acceleration-based player movement with realistic physics
- **Screen Wrapping**: Player and asteroids wrap around screen edges
- **Lumpy Asteroids**: Irregular polygon shapes instead of perfect circles for more visual variety
- **Triangular Hitbox**: Ship uses precise triangular collision detection

### Power-ups
- **Shield** (Blue): Protects from one asteroid hit (5 seconds)
- **Speed Boost** (Yellow): Increases movement speed and acceleration (10 seconds)
- **Rapid Fire** (Red): Significantly faster shooting rate (10 seconds)
- **Triple Shot** (Green): Fires three bullets in a spread pattern (10 seconds)

### Advanced Features
- **Explosion Effects**: Particle-based explosions when asteroids are destroyed
- **Bomb System**: Drop bombs (B key) that explode after 1 second, destroying nearby asteroids
- **Scoring System**: Earn 5 points for each asteroid split or destruction
- **Pause Functionality**: Press ESC to pause/unpause the game
- **Power-up Status Display**: Real-time display of active power-ups and remaining time

## Installation

### Prerequisites
- Python 3.11 or higher
- pip or uv package manager

### Setup

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   git clone https://github.com/aileks/asteroids.git
   cd asteroids
   ```

2. **Install dependencies using uv** (recommended):
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Using the main entry point:
```bash
uv run main.py
```

### Using system python:
```bash
python3 main.py
```

## Controls

| Key | Action |
|-----|--------|
| **W** | Accelerate forward |
| **A** | Rotate left |
| **D** | Rotate right |
| **SPACE** | Shoot |
| **B** | Drop bomb |
| **ESC** | Pause/Unpause |
| **R** | Restart (on game over screen) |
| **Q** | Quit (on game over screen) |

## Game Mechanics

### Scoring
- **5 points** for each asteroid split or complete destruction
- Score is displayed in the top-left corner
- Final score is shown on the game over screen

### Asteroid Behavior
- Asteroids spawn from screen edges at regular intervals
- Large asteroids split into smaller ones when shot
- Smallest asteroids are destroyed completely
- All asteroids wrap around screen edges

### Player Ship
- Acceleration-based movement (no instant speed)
- Friction applies when not accelerating
- Triangular collision detection for precise hit detection
- Wraps around screen edges

### Shots
- Shots travel in a straight line
- Shots are removed when they leave the screen (no wrapping)
- Multiple weapon types available via power-ups

### Power-ups
- Power-ups spawn randomly on the map
- Collect by flying into them
- Each power-up has a duration timer
- Active power-ups are displayed with remaining time

### Bombs
- Drop bombs with the B key
- Bombs explode after 1 second
- Destroy all asteroids within blast radius
- 3-second cooldown between bomb drops

## Development

### Code Quality
This project uses:
- **Ruff** for linting and code formatting
- Type hints throughout the codebase
- Python 3.11+ features

## Acknowledgments

- Inspired by the classic Asteroids arcade game
- Built with [Pygame](https://www.pygame.org/)

---

**Enjoy the game!**

