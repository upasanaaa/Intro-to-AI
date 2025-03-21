import tkinter as tk
import requests
import time

SERVER_URL = "http://127.0.0.1:5000"

class Kalaha:
    def __init__(self, master):
        self.master = master
        self.master.title("Kalaha Game")

        self.board = [4, 4, 4, 4, 4, 4, 0,  4, 4, 4, 4, 4, 4, 0]  
        self.prev_player = 0
        self.last_ai_move = None

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

        self.turn_label = tk.Label(self.master, text="Your Turn", font=("Arial", 16, "bold"), fg="white", bg=self.light_brown)
        self.turn_label.pack(pady=10)

        self.status_label = tk.Label(self.master, text="", font=("Arial", 14), fg="white", bg=self.light_brown)
        self.status_label.pack(pady=5)

        self.create_board()
        self.create_restart_button()
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
                        fill=self.light_wood, outline=self.tile_outline_color_enhanced, width=self.tile_outline_width)

        canvas.create_oval(12, 12, canvas_size - 12, canvas_size - 12,
                        fill="white", outline="", width=0, stipple="gray50")

        if is_restart:
            btn_text_item = canvas.create_text(canvas_size // 2, canvas_size // 2,
                                            text="Restart", font=("Arial", 14, "bold"), fill="maroon")  
        else:
            btn_text_item = canvas.create_text(canvas_size // 2, canvas_size // 2,
                                            text=str(self.board[i]), font=("Arial", 14, "bold"), fill=self.maroon)

        return {'canvas': canvas, 'text_item_id': btn_text_item, 'index': i}

    def create_board(self):
        self.frame = tk.Frame(self.master, bg=self.light_brown, padx=20, pady=20)
        self.frame.pack()

        seller_store_data = self.create_rounded_button(self.frame, 13, True)
        seller_store = seller_store_data['canvas']
        seller_store.grid(row=0, column=7, rowspan=2, padx=10, pady=5)

        buyer_store_data = self.create_rounded_button(self.frame, 6, True)
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

    def update_board(self):
        response = requests.get(f"{SERVER_URL}/get_state").json()
        self.board = response["board"]
        current_player = response["current_player"]

        if sum(self.board[:6]) == 0 or sum(self.board[7:13]) == 0:
            p1 = self.board[6] + sum(self.board[:6])
            p2 = self.board[13] + sum(self.board[7:13])
            if p1 > p2:
                self.status_label.config(text="You Win! 🎉")
            elif p2 > p1:
                self.status_label.config(text="AI Wins! 🤖")
            else:
                self.status_label.config(text="It's a Draw! 🤝")
            self.turn_label.config(text="Game Over")
        else:
            turn_message = "Your Turn"
            if self.prev_player == current_player and current_player == 0:
                turn_message = "Your Turn Again"
            self.turn_label.config(text=turn_message)
            if self.last_ai_move is not None:
                self.status_label.config(text=f"AI played pit {self.last_ai_move}")
                self.last_ai_move = None
            else:
                self.status_label.config(text="")

        for btn_data in self.buttons_data:
            index = btn_data['index']
            btn_data['canvas'].itemconfig(btn_data['text_item_id'], text=str(self.board[index]))

        self.prev_player = current_player

    def cell_click(self, i):
        response = requests.post(f"{SERVER_URL}/play_move", json={"move": i})
        if response.status_code == 200:
            data = response.json()
            self.last_ai_move = data.get("ai_move")
            prev = self.prev_player  # store before update
            self.update_board()
            self.prev_player = prev  # restore before AI update
            self.master.after(600, self.update_board)


    def restart_game(self):
        requests.get(f"{SERVER_URL}/restart")
        self.prev_player = 0
        self.last_ai_move = None
        self.update_board()
        print("Game restarted!")

root = tk.Tk()
game_gui = Kalaha(root)
root.mainloop()
