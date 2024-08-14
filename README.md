# Bullet Heaven Survivor

## Overview
This project is a 2D survival game developed using Python and Pygame. The objective of the game is to survive waves of enemies, defeat bosses, and collect power-ups to increase your character's strength and resilience.

## Table of Contents
- [Gameplay](#Gameplay)
- [Features](#Features)
- [Controls](#Controls)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [How to Run](#How-to-Run)

## Gameplay
In this game, you control a player who must survive waves of enemies. Each wave becomes progressively more challenging, with more enemies and increasing difficulty. Every fifth wave features a boss, which is tougher to defeat but drops valuable items upon defeat.

During the game, you can collect various power-ups such as Health Potions, Damage Boosts, and Health Boosts. These items help you maintain your health, increase your attack power, and enhance your maximum health.

The game ends when the player’s health reaches zero.

## Features
- **Waves of Enemies:** The game generates waves of enemies that increase in difficulty as you progress.
- **Boss Battles:** Every fifth wave introduces a boss enemy, which is more powerful than regular enemies.
- **Power-ups:** Collect power-ups that drop from defeated bosses, including Health Potions, Damage Boosts, and Health Boosts.
- **Dynamic Difficulty:** The health of enemies increases as you survive more waves.
- **Player Damage and Health Bars:** Real-time display of the player’s current damage and health.

## Controls
- **Movement:** Use the W, A, S, D keys to move the player up, left, down, and right, respectively.
- **Shooting:** Press and hold the left mouse button to shoot in the direction of the cursor.

## Installation
1. **Clone the Repository:**
```bash
git clone https://github.com/yourusername/2D-Survival-Game.git
cd 2D-Survival-Game
```
2. **Install Dependencies:** See the [Dependencies](#Dependencies) section.
3. **Run the Game:** See the [How to Run](#How-to-Run) section.

## Dependencies
- **Python 3.7+**
- **Pygame 2.0+**

You can install Pygame via pip:
```bash
pip install pygame
```

## How to Run
To start the game, simply execute the Python script:
```bash
python main_menu.py
```
Make sure you are in the project directory when running this command.