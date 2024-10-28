from tkinter import messagebox
import tkinter as tk

from yacht import YachtGame


class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ゲーム生成")
        self.geometry("400x300")

        self.player_amount_textbox = tk.Entry(self)
        self.player_amount_textbox.pack()

        self.start_button = tk.Button(self, text="Game Start", command=self.start_game)
        self.start_button.pack()

        self.game = None

    def start_game(self):
        try:
            player_amount = int(self.player_amount_textbox.get())
            if player_amount <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "入力は正の整数でお願いします。")
            return
        self.game = YachtGame(player_amount)
        self.game.ui.mainloop()

if __name__ == "__main__":
    root = MainScreen()
    root.mainloop()