import random
import math
import copy
from flask import Flask, request, jsonify

app = Flask(__name__)

class KalahaGame:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 0  # Player 1 (Human) starts

    def is_terminal(self):
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def get_winner(self):
        if not self.is_terminal():
            return None
        self.board[6] += sum(self.board[:6])
        self.board[13] += sum(self.board[7:13])
        if self.board[13] > self.board[6]:
            return 1  # AI wins
        elif self.board[6] > self.board[13]:
            return -1  # Human wins
        return 0  # Draw

    def get_valid_moves(self):
        start, end = (0, 6) if self.current_player == 0 else (7, 13)
        return [i for i in range(start, end) if self.board[i] > 0]

    def play_move(self, move):
        new_game = copy.deepcopy(self)
        seeds = new_game.board[move]
        new_game.board[move] = 0
        index = move

        while seeds > 0:
            index = (index + 1) % 14
            if index == (6 if new_game.current_player == 1 else 13):
                continue
            new_game.board[index] += 1
            seeds -= 1

        if 0 <= index < 6 and new_game.current_player == 0 and new_game.board[index] == 1:
            new_game.board[6] += new_game.board[index] + new_game.board[12 - index]
            new_game.board[index] = new_game.board[12 - index] = 0
        elif 7 <= index < 13 and new_game.current_player == 1 and new_game.board[index] == 1:
            new_game.board[13] += new_game.board[index] + new_game.board[12 - index]
            new_game.board[index] = new_game.board[12 - index] = 0

        if index != (6 if new_game.current_player == 0 else 13):
            new_game.current_player = 1 - new_game.current_player

        return new_game

class MCTSNode:
    def __init__(self, game_state, parent=None):
        self.state = game_state
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.value = 0

    def expand(self):
        if not self.children:
            for move in self.state.get_valid_moves():
                self.children[move] = MCTSNode(self.state.play_move(move), self)

    def best_child(self, exploration=1.4):
        return max(self.children.items(), key=lambda item: 
                   item[1].value / (item[1].visits + 1e-6) + 
                   exploration * math.sqrt(math.log(self.visits + 1) / (item[1].visits + 1e-6)))[0]

    def update(self, result):
        self.visits += 1
        self.value += result


def mcts_search(game, itermax=1000):
    root = MCTSNode(game)
    for _ in range(itermax):
        node = root
        while node.children and not node.state.is_terminal():
            node = node.children[node.best_child()]
        if not node.state.is_terminal():
            node.expand()
        result = simulate(node.state)
        while node:
            node.update(result)
            node = node.parent
    return root.best_child(0)

def simulate(game):
    state = copy.deepcopy(game)
    while not state.is_terminal():
        state = state.play_move(random.choice(state.get_valid_moves()))
    return state.get_winner()

# ----------------- Flask API for GUI ----------------- #
game = KalahaGame()

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify({"board": game.board, "current_player": game.current_player})

@app.route('/play_move', methods=['POST'])
def play_move():
    global game
    data = request.json
    move = data.get("move")
    if move is None or move not in game.get_valid_moves():
        return jsonify({"error": "Invalid move"}), 400
    game = game.play_move(move)
    
    # If AI's turn, make AI move automatically
    while game.current_player == 1 and not game.is_terminal():
        ai_move = mcts_search(game)
        game = game.play_move(ai_move)
    
    return jsonify({"board": game.board, "current_player": game.current_player})

@app.route('/restart', methods=['GET'])
def restart():
    global game
    game = KalahaGame()
    return jsonify({"message": "Game restarted"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
