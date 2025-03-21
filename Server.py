import random
import math
import copy
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a simple moves log file
moves_log_filename = f"kalaha_moves_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
moves_log_file = open(moves_log_filename, "w")
moves_log_file.write("=== Kalaha Game Moves Log ===\n")
moves_log_file.write(f"Game started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
moves_log_file.flush()

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

def minimax(game, depth, alpha, beta, maximizing):
    temp_board = copy.deepcopy(game.board)
    if depth == 0 or game.is_terminal():
        return temp_board[13] - temp_board[6], None

    valid_moves = game.get_valid_moves()
    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in valid_moves:
            new_game = game.play_move(move)
            eval_score, _ = minimax(new_game, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_game = game.play_move(move)
            eval_score, _ = minimax(new_game, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# ----------------- Flask API for GUI ----------------- #
game = KalahaGame()

@app.route('/get_state', methods=['GET'])
def get_state():
    # Check for game over condition and log it
    if game.is_terminal() or game.board[6] > 20 or game.board[13] > 20:
        winner_text = ""
        if game.board[6] > game.board[13]:
            winner_text = "Player wins!"
        elif game.board[13] > game.board[6]:
            winner_text = "AI wins!"
        else:
            winner_text = "It's a draw!"
            
        moves_log_file.write(f"Game over detected on state request! {winner_text}\n")
        moves_log_file.write(f"Final board: {game.board}\n\n")
        moves_log_file.flush()
    
    return jsonify({"board": game.board, "current_player": game.current_player})

@app.route('/play_move', methods=['POST'])
def play_move():
    global game
    data = request.json
    move = data.get("move")
    
    if move is None or move not in game.get_valid_moves():
        return jsonify({"error": "Invalid move"}), 400
    
    # Log player move
    moves_log_file.write(f"Player move: Pit {move}\n")
    moves_log_file.write(f"Board before: {game.board}\n")
    
    # Execute player move
    game = game.play_move(move)
    
    moves_log_file.write(f"Board after: {game.board}\n")
    moves_log_file.flush()
    
    # If AI's turn, make AI move automatically
    while game.current_player == 1 and not game.is_terminal():
        # Use minimax with depth 6 for AI
        _, ai_move = minimax(game, 6, float('-inf'), float('inf'), True)
        
        if ai_move is not None:
            # Log AI move
            moves_log_file.write(f"AI move: Pit {ai_move}\n")
            moves_log_file.write(f"Board before: {game.board}\n")
            
            # Execute AI move
            game = game.play_move(ai_move)
            
            moves_log_file.write(f"Board after: {game.board}\n")
            moves_log_file.flush()
    
    # Check for game terminal state
    if game.is_terminal():
        winner = game.get_winner()
        winner_text = "AI" if winner == 1 else "Human" if winner == -1 else "Draw"
        moves_log_file.write(f"Game over. Winner: {winner_text}\n")
        moves_log_file.write(f"Final score - Player: {game.board[6]}, AI: {game.board[13]}\n\n")
        moves_log_file.flush()
    
    # Also check for scoring threshold game over (score > 20)
    if game.board[6] > 20 or game.board[13] > 20:
        winner_text = "Player" if game.board[6] > game.board[13] else "AI"
        moves_log_file.write(f"Game over by score threshold. Winner: {winner_text}\n")
        moves_log_file.write(f"Final score - Player: {game.board[6]}, AI: {game.board[13]}\n\n")
        moves_log_file.flush()
    
    return jsonify({"board": game.board, "current_player": game.current_player})

@app.route('/restart', methods=['GET'])
def restart():
    global game
    
    moves_log_file.write("\n=== New Game ===\n")
    moves_log_file.write(f"Game restarted at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    moves_log_file.flush()
    
    game = KalahaGame()
    return jsonify({"message": "Game restarted"})


if __name__ == "__main__":
    print(f"Kalaha Game Server starting. Moves log file: {moves_log_filename}")
    
    try:
        app.run(host="127.0.0.1", port=5000, debug=True)
    finally:
        # Close the log file when the server shuts down
        moves_log_file.close()