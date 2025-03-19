import tkinter as tk

class KalahaGUI:
    def _init_(self, master):
        self.master = master
        self.master.title("Kalaha Game")

        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # Starting board

        self.buttons = self.create_buttons()
        self.update_board()

    def create_buttons(self):
        """ Create GUI buttons for the Kalaha game """
        buttons = []
        for i in range(14):  # 6 pits for each player + 2 stores
            button = tk.Button(self.master, text=str(self.board[i]), width=10, height=3,
                               command=lambda i=i: self.cell_click(i))
            button.grid(row=i // 7, column=i % 7, padx=5, pady=5)
            buttons.append(button)
        return buttons

    def update_board(self):
        """ Update the board display """
        for i in range(14):
            self.buttons[i].config(text=str(self.board[i]))

    def cell_click(self, i):
        """ Placeholder for game logic when clicking on a cell """
        print(f"Pit {i} clicked!")
        # Call the backend API to update the game state here

    def add_random_tile(self):
        """ Add a random tile in an empty spot (for Kalaha) """
        # This logic could be added to simulate random tile addition, or player turns.


# Main game window
root = tk.Tk()
game_gui = KalahaGUI(root)
root.mainloop()