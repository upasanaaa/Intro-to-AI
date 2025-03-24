```
# Kalaha Game - AI vs Human

A simple and fun Kalaha (Mancala) board game where you play against an AI powered by the Minimax algorithm with alpha-beta pruning.
Built with Python, Flask, and Tkinter.

---

## Features

- Classic Kalaha (Mancala) gameplay
- Play against AI with a clean, user-friendly GUI
- AI strategy powered by Minimax with Alpha-Beta pruning for optimized decision-making
- Smooth gameplay experience using Flask for backend logic and Tkinter for the frontend interface
- Game ends when one player captures more than 50% of the stones or one side is empty
- Move history and current game status are displayed clearly

---

## Requirements

To run this project, you'll need Python 3.9 or higher, along with the following libraries:

- Flask for the backend
- Requests for handling HTTP requests between the frontend and backend
- Tkinter for the GUI (comes pre-installed with Python on most systems)
```
## Project Structure

```
Intro-to-AI/
├── GUI.py            # GUI built with Tkinter
├── server.py         # Backend logic with Flask and AI
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

---

## Installation

Install dependencies:
   Make sure you're using a virtual environment for this project (recommended).

   To install dependencies, use:

   ```bash
   pip install -r requirements.txt
   

   Alternatively, you can install them manually by running:

   ```bash
   pip install flask requests
   ```

---

## How to Run the Game

### 1. Clone the Repository
```bash
git clone https://github.com/upasanaaa/Intro-to-AI.git
cd Intro-to-AI
```

### 2. (Optional) Create a Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Flask Server (Backend)
```bash
python server.py
```

### 5. Launch the GUI (Frontend)
Let the `server.py` run and open a new terminal window and run:
```bash
python GUI.py
```

---

## Notes for macOS/Linux Users

- Use `python` instead of `python3` if needed:
```bash
python3 server.py
python3 GUI.py
```

- If Tkinter is not installed, use the following commands:

  - On **Ubuntu/Debian**:
    ```bash
    sudo apt-get install python3-tk
    ```

  - On **macOS** with Homebrew:
    ```bash
    brew install python-tk
    ```

---

## Game Rules

- The board consists of 14 pits: 6 on each side for both players, and 2 stores (**Kalahs**).
- Each pit starts with 4 stones.
- Players take turns sowing stones counter-clockwise.
- Drop one stone per pit, including your Kalah but skip your opponent’s Kalah.
- If your last stone lands in your own empty pit and the opposite pit has stones, both are captured.
- If your last stone lands in your Kalah, you get another turn.
- The game ends when:
  - A player has no stones left to play.
  - OR a player collects more than 50% of the total stones (e.g., 25 out of 48).

---

## How the AI Works

- Implements the **Minimax** algorithm with a configurable depth limit.
- Uses **alpha-beta pruning** to optimize the search by pruning branches that do not need to be explored.
- The **heuristic function** is based on the current score + half of the remaining seeds on the board.

For a detailed explanation of the Minimax algorithm, please refer to [this resource](https://en.wikipedia.org/wiki/Minimax).

---

## Troubleshooting

- **Flask** not installed? → `pip install flask`
- **Requests** missing? → `pip install requests`
- **GUI** not opening? Ensure `server.py` is running in a separate terminal window.
- **Tkinter** not found? → Install Tkinter using the instructions above for your system.
- Contact us if needed!