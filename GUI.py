import tkinter as tk
import copy
import requests

SERVER_URL = "http://127.0.0.1:5000"

class Kalaha:
    def __init__(self, master):
        self.master = master
        self.master.title("Kalaha Game")

        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # 0-5 Player, 6 Kalah, 7-12 AI, 13 Kalah
        self.current_player = 0  # 0: Player, 1: AI
        self.last_ai_move = None
        self.game_over = False  # Flag to track if game is over

        self.light_brown = "#D2691E"
        self.maroon = "maroon"
        self.light_wood = "#D2B48C"
        self.shadow_color = "#800000"
        self.tile_outline_color_enhanced = "#5E3A29"
        self.shadow_offset_x = 3
        self.shadow_offset_y = 3
        self.tile_outline_width = 1.5

        self.buttons_data = []

        self.master.configure(bg=self.light_brown)

        self.turn_label = tk.Label(self.master, text="Your Turn", font=("Arial", 16, "bold"),
                                   fg="white", bg=self.light_brown)
        self.turn_label.pack(pady=10)

        self.status_label = tk.Label(self.master, text="", font=("Arial", 14),
                                     fg="white", bg=self.light_brown)
        self.status_label.pack(pady=5)

        self.create_board()
        self.create_restart_button()
        self.create_move_log()
        self.update_board()

    def create_rounded_button(self, parent, i, is_store=False, is_restart=False):
        canvas_size = 70 if is_store else 60
        if is_restart:
            canvas_size = 90

        canvas = tk.Canvas(parent, width=canvas_size, height=canvas_size,
                        bg=self.light_brown, highlightthickness=0)

        canvas.create_oval(4 + self.shadow_offset_x, 4 + self.shadow_offset_y,
                           canvas_size - 4 + self.shadow_offset_x, canvas_size - 4 + self.shadow_offset_y,
                           fill=self.shadow_color, outline="", width=0)

        canvas.create_oval(5, 5, canvas_size - 5, canvas_size - 5,
                           fill=self.light_wood, outline=self.tile_outline_color_enhanced,
                           width=self.tile_outline_width)

        canvas.create_oval(12, 12, canvas_size - 12, canvas_size - 12,
                           fill="white", outline="", width=0, stipple="gray50")

        btn_text_item = canvas.create_text(canvas_size // 2, canvas_size // 2,
                                           text="Restart" if is_restart else str(self.board[i]),
                                           font=("Arial", 14, "bold"), fill=self.maroon)

        return {'canvas': canvas, 'text_item_id': btn_text_item, 'index': i}

    def create_board(self):
        self.frame = tk.Frame(self.master, bg=self.light_brown, padx=20, pady=20)
        self.frame.pack()

        seller_store_data = self.create_rounded_button(self.frame, 6, True)
        seller_store = seller_store_data['canvas']
        seller_store.grid(row=0, column=7, rowspan=2, padx=10, pady=5)

        buyer_store_data = self.create_rounded_button(self.frame, 13, True)
        buyer_store = buyer_store_data['canvas']
        buyer_store.grid(row=0, column=0, rowspan=2, padx=10, pady=5)

        self.buttons_data.append(buyer_store_data)
        self.buttons_data.append(seller_store_data)

        for i, col in zip(range(12, 6, -1), range(1, 7)):
            btn_data = self.create_rounded_button(self.frame, i)
            btn = btn_data['canvas']
            btn.grid(row=0, column=col, padx=5, pady=5)
            btn.bind("<Button-1>", lambda event, index=i: self.cell_click(index))
            self.buttons_data.append(btn_data)

        for i, col in zip(range(0, 6), range(1, 7)):
            btn_data = self.create_rounded_button(self.frame, i)
            btn = btn_data['canvas']
            btn.grid(row=1, column=col, padx=5, pady=5)
            btn.bind("<Button-1>", lambda event, index=i: self.cell_click(index))
            self.buttons_data.append(btn_data)

    def create_restart_button(self):
        self.restart_button_data = self.create_rounded_button(self.master, None, is_restart=True)
        self.restart_button = self.restart_button_data['canvas']
        self.restart_button.pack(pady=10)
        self.restart_button.bind("<Button-1>", lambda event: self.restart_game())

    def create_move_log(self):
        self.move_log = tk.Text(self.master, height=10, width=40, font=("Arial", 12), bg=self.light_wood)
        self.move_log.pack(pady=10)
        self.move_log.insert(tk.END, "Move History:\n")
        self.move_log.config(state=tk.DISABLED)

    def log_move(self, text):
        self.move_log.config(state=tk.NORMAL)
        self.move_log.insert(tk.END, text + "\n")
        self.move_log.see(tk.END)
        self.move_log.config(state=tk.DISABLED)

    def update_board(self):
        # Get game state from server if not already updated
        if not hasattr(self, 'just_updated') or not self.just_updated:
            response = requests.get(f"{SERVER_URL}/get_state").json()
            self.board = response["board"]
            self.current_player = response["current_player"]
        else:
            self.just_updated = False

        # Update the visual representation of the board
        for btn_data in self.buttons_data:
            index = btn_data['index']
            btn_data['canvas'].itemconfig(btn_data['text_item_id'], text=str(self.board[index]))

        if self.current_player == 1 and not self.game_over:
            self.turn_label.config(text="AI's Turn")
        else:
            self.turn_label.config(text="Your Turn")

        if self.board[6] > 20 or self.board[13] > 20:
            winner = "AI Win! 🎉" if self.board[13] > self.board[6] else "You Win! 🎉"
            self.status_label.config(text=winner)
            self.turn_label.config(text="Game Over")
            self.game_over = True
            return

    def cell_click(self, i):
        if self.game_over or self.current_player != 0 or self.board[i] == 0 or i > 5:
            return
        
        # Save previous board state
        prev_board = self.board.copy()
        
        # Log the move
        self.log_move(f"You: Pit {i}")
        
        # Send the move to the server
        response = requests.post(f"{SERVER_URL}/play_move", json={"move": i}).json()
        
        # Get the updated board state
        self.board = response["board"]
        self.current_player = response["current_player"]
        
        # Compare boards to find AI move
        for j in range(7, 13):
            if prev_board[j] > 0 and self.board[j] == 0:
                # AI likely moved from this pit
                self.log_move(f"AI: Pit {j}")
                break
        
        # Update the board display
        self.update_board()

    def restart_game(self):
        requests.get(f"{SERVER_URL}/restart")
        self.board = [4, 4, 4, 4, 4, 4, 0,  4, 4, 4, 4, 4, 4, 0]
        self.current_player = 0
        self.last_ai_move = None
        self.game_over = False  # Reset game over flag
        self.update_board()
        self.move_log.config(state=tk.NORMAL)
        self.move_log.delete("1.0", tk.END)
        self.move_log.insert(tk.END, "Move History:\n")
        self.move_log.config(state=tk.DISABLED)
        self.status_label.config(text="")
        self.turn_label.config(text="Your Turn")

        

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game_gui = Kalaha(root)
    root.mainloop()