import tkinter as tk
import requests
import time

SERVER_URL = "http://127.0.0.1:5000"

class Kalaha:
    def __init__(self, master):
        self.master = master
        self.master.title("Kalaha Game")

        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 0
        self.game_over = False

        self.setup_colors()
        self.master.configure(bg=self.light_brown)

        self.turn_label = self.make_label("Your Turn", 16, bold=True)
        self.status_label = self.make_label("", 14)
        self.create_labels()
        


        self.buttons_data = []
        self.create_board()
        self.create_restart_button()
        self.create_move_log()
        self.update_board()

    def setup_colors(self):
        self.light_brown = "#D2691E"
        self.maroon = "maroon"
        self.light_wood = "#D2B48C"
        self.shadow_color = "#800000"
        self.tile_outline_color_enhanced = "#5E3A29"
        self.shadow_offset_x = 3
        self.shadow_offset_y = 3
        self.tile_outline_width = 1.5

    def make_label(self, text, size, bold=False):
        font = ("Arial", size, "bold") if bold else ("Arial", size)
        label = tk.Label(self.master, text=text, font=font, fg="white", bg=self.light_brown)
        label.pack(pady=5)
        return label
    
    def create_labels(self):
        label_frame = tk.Frame(self.master, bg=self.light_brown)
        label_frame.pack(pady=(5, 0))
        tk.Label(label_frame, text="← AI Side", font=("Arial", 12), fg="white", bg=self.light_brown).pack(side=tk.LEFT, expand=True)

    def create_rounded_button(self, parent, i, is_store=False, is_restart=False):
        canvas_size = 90 if is_restart else (70 if is_store else 60)
        canvas = tk.Canvas(parent, width=canvas_size, height=canvas_size, bg=self.light_brown, highlightthickness=0)

        canvas.create_oval(4 + self.shadow_offset_x, 4 + self.shadow_offset_y,
                           canvas_size - 4 + self.shadow_offset_x, canvas_size - 4 + self.shadow_offset_y,
                           fill=self.shadow_color, outline="")
        canvas.create_oval(5, 5, canvas_size - 5, canvas_size - 5,
                           fill=self.light_wood, outline=self.tile_outline_color_enhanced, width=self.tile_outline_width)
        canvas.create_oval(12, 12, canvas_size - 12, canvas_size - 12,
                           fill="white", outline="", stipple="gray50")

        text = "Restart" if is_restart else str(self.board[i])
        text_item = canvas.create_text(canvas_size // 2, canvas_size // 2, text=text, font=("Arial", 14, "bold"), fill=self.maroon)
        return {'canvas': canvas, 'text_item_id': text_item, 'index': i}

    def create_board(self):
        self.frame = tk.Frame(self.master, bg=self.light_brown, padx=20, pady=20)
        self.frame.pack()

        self.buttons_data.append(self.create_rounded_button(self.frame, 13, is_store=True))
        self.buttons_data[0]['canvas'].grid(row=0, column=0, rowspan=2, padx=10, pady=5)

        self.buttons_data.append(self.create_rounded_button(self.frame, 6, is_store=True))
        self.buttons_data[1]['canvas'].grid(row=0, column=7, rowspan=2, padx=10, pady=5)

        for i, col in zip(range(12, 6, -1), range(1, 7)):
            btn_data = self.create_rounded_button(self.frame, i)
            btn_data['canvas'].grid(row=0, column=col, padx=5, pady=5)
            btn_data['canvas'].bind("<Button-1>", lambda event, index=i: self.cell_click(index))
            self.buttons_data.append(btn_data)

        for i, col in zip(range(0, 6), range(1, 7)):
            btn_data = self.create_rounded_button(self.frame, i)
            btn_data['canvas'].grid(row=1, column=col, padx=5, pady=5)
            btn_data['canvas'].bind("<Button-1>", lambda event, index=i: self.cell_click(index))
            self.buttons_data.append(btn_data)

    def create_restart_button(self):
        tk.Label(self.master, text="Player Side →", font=("Arial", 12), fg="white", bg=self.light_brown).pack(pady=(10, 2))
        btn_data = self.create_rounded_button(self.master, None, is_restart=True)
        btn = btn_data['canvas']
        btn.pack(pady=10)
        btn.bind("<Button-1>", lambda event: self.restart_game())

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
        response = requests.get(f"{SERVER_URL}/get_state").json()
        self.board = response["board"]
        self.current_player = response["current_player"]

        for btn_data in self.buttons_data:
            index = btn_data['index']
            btn_data['canvas'].itemconfig(btn_data['text_item_id'], text=str(self.board[index]))

        if self.current_player == 1 and not self.game_over:
            self.turn_label.config(text="AI's Turn")
        elif not self.game_over:
            self.turn_label.config(text="Your Turn")

        if self.board[6] > 25 or self.board[13] > 25:
            winner = "AI Wins! 🎉" if self.board[13] > self.board[6] else "You Win! 🎉"
            self.status_label.config(text=winner)
            self.turn_label.config(text="Game Over")
            self.game_over = True

    def cell_click(self, i):
        if self.game_over or self.current_player != 0 or self.board[i] == 0 or i > 5:
            return

        prev_board = self.board.copy()
        self.log_move(f"You -> {i+1}")
        response = requests.post(f"{SERVER_URL}/play_move", json={"move": i}).json()

        self.board = response["board"]
        self.current_player = response["current_player"]

        # Detect AI move by comparing pits
        if self.current_player == 0:
            for j in range(7, 13):
                if prev_board[j] > 0 and self.board[j] == 0:
                    self.log_move(f"AI -> {j+1}")
                    break

        self.update_board()  # Only call once, avoid duplicate Game Over
        if not self.game_over:
            time.sleep(1)
            self.update_board()  # Delay to visualize AI move
        self.update_board()

    def restart_game(self):
        requests.get(f"{SERVER_URL}/restart")
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 0
        self.game_over = False
        self.update_board()
        self.move_log.config(state=tk.NORMAL)
        self.move_log.delete("1.0", tk.END)
        self.move_log.insert(tk.END, "Move History:\n")
        self.move_log.config(state=tk.DISABLED)
        self.status_label.config(text="")
        self.turn_label.config(text="Your Turn")


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = Kalaha(root)
    root.mainloop()