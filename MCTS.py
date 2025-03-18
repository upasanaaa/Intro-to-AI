import random
import math
import copy

class KalahaGame:
    def __init__(self):
        """Initialize the Kalaha board."""
        self.board = [4] * 6 + [0] + [4] * 6 + [0]  # 6 pits per player + 2 stores
        self.current_player = 0  # Player 0 (Human) starts

    def is_terminal(self):
        """Check if the game is over (one side is empty)."""
        return sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0

    def get_winner(self):
        """Determine the winner: 1 (AI), -1 (Human), 0 (Draw)."""
        if not self.is_terminal():
            return None
        # Move remaining seeds to respective stores
        self.board[6] += sum(self.board[:6])
        self.board[13] += sum(self.board[7:13])

        if self.board[13] > self.board[6]:
            return 1  # AI wins
        elif self.board[6] > self.board[13]:
            return -1  # Human wins
        return 0  # Draw

    def get_valid_moves(self):
        """Return a list of valid moves for the current player."""
        start, end = (0, 6) if self.current_player == 0 else (7, 13)
        return [i for i in range(start, end) if self.board[i] > 0]

    def play_move(self, move):
        """Execute a move and return the new game state."""
        new_game = copy.deepcopy(self)
        seeds = new_game.board[move]
        new_game.board[move] = 0
        index = move

        while seeds > 0:
            index = (index + 1) % 14
            if index == (6 if new_game.current_player == 1 else 13):  # Skip opponent's store
                continue
            new_game.board[index] += 1
            seeds -= 1

        # Capture rule
        if 0 <= index < 6 and new_game.current_player == 0 and new_game.board[index] == 1:
            new_game.board[6] += new_game.board[index] + new_game.board[12 - index]
            new_game.board[index] = new_game.board[12 - index] = 0
        elif 7 <= index < 13 and new_game.current_player == 1 and new_game.board[index] == 1:
            new_game.board[13] += new_game.board[index] + new_game.board[12 - index]
            new_game.board[index] = new_game.board[12 - index] = 0

        # Extra turn rule
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
        """Expand the node by adding children for valid moves."""
        if not self.children:
            for move in self.state.get_valid_moves():
                self.children[move] = MCTSNode(self.state.play_move(move), self)

    def best_child(self, exploration=1.4):
        """Select the best child using UCB1 formula."""
        return max(self.children.items(), key=lambda item: 
                   item[1].value / (item[1].visits + 1e-6) + 
                   exploration * math.sqrt(math.log(self.visits + 1) / (item[1].visits + 1e-6)))[0]

    def update(self, result):
        """Update node statistics after a simulation."""
        self.visits += 1
        self.value += result

def mcts_search(game, itermax=1000):
    """Run Monte Carlo Tree Search (MCTS) and return the best move."""
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
    """Simulate a random game from the current state and return the result."""
    state = copy.deepcopy(game)
    while not state.is_terminal():
        state = state.play_move(random.choice(state.get_valid_moves()))
    return state.get_winner()

def print_board(game):
    """Display the current board state in a readable format."""
    print("\n  AI (P1)")
    print("  ", "  ".join(map(str, game.board[12:6:-1])))
    print(f"{game.board[13]} --------------- {game.board[6]}")
    print("  ", "  ".join(map(str, game.board[:6])))
    print("You (P0)\n")

# ----------------- Game Loop ----------------- #
game = KalahaGame()

print("Welcome to Kalaha! You are Player 0 (Bottom Side).")
print_board(game)

while not game.is_terminal():
    if game.current_player == 0:
        move = int(input("Your move (0-5): "))  # Human move
        while move not in game.get_valid_moves():
            print("Invalid move. Try again.")
            move = int(input("Your move (0-5): "))
    else:
        move = mcts_search(game, itermax=1000)  # AI Move
        print(f"AI plays: {move}")

    game = game.play_move(move)
    print_board(game)

# Determine and announce winner
winner = game.get_winner()
if winner == 1:
    print("Game Over! 🎉 The AI Wins!")
elif winner == -1:
    print("Game Over! 🎉 You Win!")
else:
    print("Game Over! 🤝 It's a Draw!")
