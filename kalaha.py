import tkinter as tk

class Kalaha:
    def __init__(self, master):
        self.master = master
        self.master.title("Kalaha Game")

        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # Starting board

        self.light_brown = "#D2691E"        # Lighter brown color for the background
        self.maroon = "maroon"              # Maroon color for numbers
        self.light_wood = "#D2B48C"         # Light Wood Color for tiles
        self.shadow_color = "#800000"       # Darker shadow color
        self.tile_outline_color_enhanced = "#5E3A29"  # Darker brown outline
        self.shadow_offset_x = 3
        self.shadow_offset_y = 3
        self.tile_outline_width = 1.5

        self.buttons_data = []  # Store button data

        self.master.configure(bg=self.light_brown)  # Set background color

        self.create_board()
        self.create_restart_button()  # Create restart button after the board
        self.update_board()

    def create_rounded_button(self, parent, i, is_store=False, is_restart=False):
        canvas_size = 70 if is_store else 60
        if is_restart:
            canvas_size = 90  # Increase restart button size

        canvas = tk.Canvas(parent, width=canvas_size, height=canvas_size,
                        bg=self.light_brown, highlightthickness=0)

        # Create shadow
        canvas.create_oval(4 + self.shadow_offset_x, 4 + self.shadow_offset_y,
                        canvas_size - 4 + self.shadow_offset_x, canvas_size - 4 + self.shadow_offset_y,
                        fill=self.shadow_color, outline="", width=0)

        # Create main oval (tile)
        canvas.create_oval(5, 5, canvas_size - 5, canvas_size - 5,
                        fill=self.light_wood, outline=self.tile_outline_color_enhanced, width=self.tile_outline_width)

        # Glossy effect
        canvas.create_oval(12, 12, canvas_size - 12, canvas_size - 12,
                        fill="white", outline="", width=0, stipple="gray50")

        if is_restart:
            btn_text_item = canvas.create_text(canvas_size // 2, canvas_size // 2,
                                            text="Restart", font=("Arial", 14, "bold"), fill="maroon")  # Larger text
        else:
            btn_text_item = canvas.create_text(canvas_size // 2, canvas_size // 2,
                                            text=str(self.board[i]), font=("Arial", 14, "bold"), fill=self.maroon)

        return {'canvas': canvas, 'text_item_id': btn_text_item}

    def create_board(self):
        """ Create GUI board layout """
        self.frame = tk.Frame(self.master, bg=self.light_brown, padx=20, pady=20)
        self.frame.pack()

        # Create stores
        seller_store_data = self.create_rounded_button(self.frame, 13, True)
        seller_store = seller_store_data['canvas']
        seller_store.grid(row=0, column=7, rowspan=2, padx=10, pady=5)

        buyer_store_data = self.create_rounded_button(self.frame, 6, True)
        buyer_store = buyer_store_data['canvas']
        buyer_store.grid(row=0, column=0, rowspan=2, padx=10, pady=5)

        self.buttons_data.append(buyer_store_data)
        self.buttons_data.append(seller_store_data)

        # Upper row (Seller)
        for i in range(12, 6, -1):
            btn_data = self.create_rounded_button(self.frame, i)
            btn = btn_data['canvas']
            btn.grid(row=0, column=12 - i + 1, padx=5, pady=5)
            self.buttons_data.append(btn_data)

        # Lower row (Buyer)
        for i in range(6):
            btn_data = self.create_rounded_button(self.frame, i)
            btn = btn_data['canvas']
            btn.grid(row=1, column=i + 1, padx=5, pady=5)
            self.buttons_data.append(btn_data)

    def create_restart_button(self):
        """ Create a restart button matching the style of other tiles """
        self.restart_button_data = self.create_rounded_button(self.master, None, is_restart=True)
        self.restart_button = self.restart_button_data['canvas']
        self.restart_button.pack(pady=10)
        self.restart_button.bind("<Button-1>", lambda event: self.restart_game())

    def update_board(self):
        """ Update the board display """
        for i in range(14):
            if self.buttons_data[i]['text_item_id']:
                self.buttons_data[i]['canvas'].itemconfig(self.buttons_data[i]['text_item_id'], text=str(self.board[i]))

    def cell_click(self, i):
        """ Placeholder for game logic """
        print(f"Pit {i} clicked!")

    def restart_game(self):
        """ Restart the game by resetting the board """
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # Reset board
        self.update_board()
        print("Game restarted!")

# Main game window
root = tk.Tk()
game_gui = Kalaha(root)
root.mainloop()
