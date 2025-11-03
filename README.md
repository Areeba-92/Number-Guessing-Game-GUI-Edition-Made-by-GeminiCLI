# Number Guessing Game 🎯

A fun, interactive number guessing game built with Python and Tkinter.
Features include multiple difficulty levels, personalized greetings, custom themes, a leaderboard, save/load functionality, and even an AI opponent mode. 

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Modes](#game-modes)
- [Leaderboard](#leaderboard)
- [Instructions](#instructions)
- [Themes](#themes)


---

## Features
- Multiple difficulty levels: Easy, Medium, Hard.
- Dynamic hints when attempts are low.
- Save and load game progress.
- AI opponent mode: the AI guesses your number!
- Animated feedback for guesses.
- Adjustable range based on performance.
- Fully themed interface (Light, Dark, Neon, Neutral).
- Leaderboard to track top scores.

---

## Installation

1. Make sure you have **Python 3.x** installed on your system.
2. Clone this repository:

```
git clone https://github.com/yourusername/number-guessing-game.git
```
Navigate into the project directory:

```
cd number-guessing-game
```
Install required dependencies (Tkinter is usually included with Python):

```
# Tkinter comes pre-installed with Python on most systems.
# If not, install using your package manager, e.g., for Ubuntu:
sudo apt install python3-tk
```
# Usage
Run the game with:

```
python number_guessing_game.py
```
Follow the on-screen instructions to enter your name and start playing!

# Game Modes
- **Single Player Mode**: Guess the randomly generated number within a limited number of attempts.

- **AI Opponent Mode**: Think of a number, and the AI will try to guess it based on your feedback (Higher / Lower / Correct).

# Leaderboard
- The game tracks top scores and displays them in a leaderboard.

- Scores are based on attempts, time taken, and difficulty level.

**The leaderboard is stored in leaderboard.txt.**

# Instructions
- Enter your name to start the game.

- Choose a difficulty level:

  - **Easy**: 1–50 (10 attempts)

  - **Medium**: 1–100 (7 attempts)

  - **Hard**: 1–200 (5 attempts)

- Try to guess the secret number within the allowed attempts.

- Hints will appear when attempts are running out.

- Save your game anytime and continue later.

- Compete for a high score to make it onto the leaderboard.

# Themes
- The game supports **multiple visual themes**:

   - Light

   - Dark

   - Neutral

   - Neon

Change themes anytime from the menu for a personalized experience.
