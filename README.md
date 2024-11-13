# Animal Ambush (Unfinished)

A turn-based strategy game developed in Python using Pygame. In Animal Ambush, players control various animal units with different roles and strengths, battling it out on a dynamically rendered game board. The game uses a unique 3D sprite stacking technique to simulate depth and rotation for an engaging visual experience.

## Features

- **Turn-Based Strategy**: Players take turns controlling animal troops to conquer territories and attack opponents.
- **3D Sprite Stack Rendering**: Uses layered sprites with rotation to create a 3D-like visual depth effect.
- **Dynamic Camera Controls**: The camera can zoom, pan, and rotate, allowing players to explore the game map smoothly.
- **Customizable Settings**: Configure game resolution, frame rate, and camera options.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

Install Pygame using pip:
```bash
pip install pygame
```

### Installation
1. **Clone this repository**:
2. **Run the game**:
    ```bash
    python main.py
    ```

## **Usage**
- **Camera Control**: Use mouse movements and clicks to pan, zoom, and rotate the camera.
- **Troop Selection**: Click on a troop to view movement options; use selection boxes to move troops.
- **Gameplay**: Engage with enemy troops, capture territory, and utilize each unit type's unique abilities.

## **Game Controls**
- **Left Mouse Button**: Select and move troops.
- **Right Mouse Button**: Rotate the camera view.
- **Mouse Wheel**: Zoom in and out.

## **Game Settings**
Configure game settings in ```settings.py```:

- **WINDOW_SIZE**: Set screen resolution.
- **FPS**: Configure frame rate.
- **CAMERA_ZOOM_MAX**: Adjust maximum zoom level.
- **STACK_CACHE_ENABLED**: Enable or disable caching for faster rendering.

## Project Structure
- **main.py**: Initializes the game window and starts the game loop.
- **game.py**: Manages the main game loop and interactions.
- **camera.py**: Handles camera movement, zoom, and rotation.
- **troop.py**: Defines the troop class with movement, selection, and combat functions.
- **highlightbox.py**: Manages selection and highlight effects for available moves.
- **levelhandler.py**: Generates and renders the level map with ground and corner detection.
- **spritestack.py**: Renders 3D sprite stacks for troops and map elements.