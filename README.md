# Kalaha Game - AI vs Human

A simple and fun Kalaha (Mancala) board game where you play against an AI using the Minimax algorithm with alpha-beta pruning. Built with Python, Flask, and Tkinter.

---

## Features

- Classic Kalaha (Mancala) gameplay
- Play against AI with a clean GUI
- AI strategy powered by Minimax with Alpha-Beta pruning
- Smooth gameplay using Flask for backend and Tkinter for frontend
- Game ends when one player has over 50% of the stones or one side is empty
- Move history is displayed clearly

---

## Requirements

- Python 3.9 or higher
- Flask
- Requests
- Tkinter (usually comes pre-installed with Python)

Install all required packages using:
```bash
pip install -r requirement.txt
```
Or install them manually:
```bash
pip install flask requests
```

---

## Project Structure

```
Intro-to-AI/
├── GUI.py            # GUI built with Tkinter
├── server.py         # Backend logic with Flask and AI
├── requirement.txt   # Python dependencies
└── README.md         # Project documentation
```

---

## 💻 How to Run the Game

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Intro-to-AI.git
cd Intro-to-AI
```

### 2. (Optional) Create a Virtual Environment

**On Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**
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
Open a new terminal window and run:
```bash
python GUI.py
```

---

## Notes for macOS/Linux Users

- Use `python3` instead of `python` if needed:
```bash
python3 server.py
python3 GUI.py
```

- If Tkinter is not installed:
  - On Ubuntu/Debian:
    ```bash
    sudo apt-get install python3-tk
    ```
  - On macOS with Homebrew:
    ```bash
    brew install python-tk
    ```

---

## Game Rules

- The board consists of 14 pits: 6 on each side and 2 stores (Kalahs)
- Each pit starts with 4 stones
- Players take turns sowing stones counter-clockwise
- Drop one stone per pit, including your Kalah but **skip your opponent’s Kalah**
- If your last stone lands in your own empty pit and the opposite pit has stones, both are captured
- If your last stone lands in your Kalah, you get another turn
- The game ends when:
  - A player has no stones left to play
  - OR a player collects more than 50% of the total stones (e.g., 25 out of 48)

---

## How the AI Works

- Implements Minimax algorithm with depth limit
- Uses alpha-beta pruning to optimize search
- Heuristic function: current score + half of remaining seeds on the board

---

## Troubleshooting

- Flask not installed? → `pip install flask`
- Requests missing? → `pip install requests`
- GUI not opening? Ensure `server.py` is running in a separate terminal

---
