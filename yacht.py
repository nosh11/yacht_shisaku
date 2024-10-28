import random
import tkinter as tk
import customtkinter as ctk

from player import Player
from settings import HANDS, getScore

class YachtGame:
    def __init__(self, players_amount: int):
        self.__players = [Player(f"{i+1}P") for i in range(players_amount)]
        self.__current_player_idx = 0
        self.__turn = 0
        self.__dice = [0, 0, 0, 0, 0]
        self.__ui = YachtGameUI(self)

        self.player_turn()
    
    def next(self):
        self.__current_player_idx = (self.__current_player_idx + 1) % len(self.__players)
        self.player_turn()


    def player_turn(self):
        self.ui.turn_label.configure(text=f"{self.current_player.getName()}のターン")
        print(f"player_idx = {self.current_player_idx}, turn = {self.turn}")
        self.roll_dice()


    @property
    def players(self):
        return self.__players
    
    @property
    def current_player(self):
        return self.__players[self.__current_player_idx]
    
    @property
    def current_player_idx(self):
        return self.__current_player_idx
    
    @property
    def turn(self):
        return self.__turn
    
    @property
    def dice(self):
        return self.__dice
    
    @dice.setter
    def dice(self, value):
        if len(value) != 5 or not all(isinstance(i, int) and 1 <= i <= 6 for i in value):
            raise ValueError("Dice must be a list of 5 integers between 1 and 6.")
        self.__dice = value
        self.ui.update_dice_label()
        self.ui.show_players_score()
    
    @property
    def ui(self):
        return self.__ui

    def show_players_score(self):
        for i in range(12):
            self.score_table.insert("", "end", iid=i, values=[HANDS[i]] + [(p.getScore(i) if p.getScore(i) is not None else "") for p in self.__players])

    def roll_dice(self, dice: list = [None, None, None, None, None]):
        dice = dice.copy()
        for i in range(5):
            if dice[i] is None:
                dice[i] = random.randint(1, 6)
        self.dice = dice


    def setScore(self, player_idx: int, hand_idx: int, score: int):
        print(f"setScore: {player_idx}, hand_idx: {hand_idx}, score: {score}")
        player = self.players[player_idx]
        player.setScore(hand_idx, score)
        self.ui.score_frame.grid_slaves(row=len(HANDS)+1, column=player_idx+1)[0].configure(
            text=str(sum([n for n in player.score if n != None])))
        self.next()

class YachtGameUI(ctk.CTk):
    def __init__(self, yacht_game : YachtGame):
        super().__init__()

        # 最前面に表示
        self.attributes("-topmost", True)

        self.__yacht = yacht_game

        self.title("Yacht Dice Game")
        self.geometry("1280x720")

        self.main_frame = ctk.CTkFrame(self)

        self.info_frame = ctk.CTkFrame(self.main_frame)

        self.turn_label = ctk.CTkLabel(self.info_frame, text="プレイヤーのターン")
        self.turn_label.pack()
        self.info_frame.pack()

        self.dice_frame = ctk.CTkFrame(self.main_frame)

        self.dice_label = ctk.CTkLabel(self.dice_frame, anchor="s", text="Dice: [0, 0, 0, 0, 0]")
        self.dice_label.pack()
        self.roll_button = ctk.CTkButton(self.dice_frame, text="Roll Dice Again", command=self.yacht.roll_dice)
        self.roll_button.pack()
        self.dice_frame.pack()

        self.score_frame = ctk.CTkFrame(self.main_frame)

        for i in range(len(self.yacht.players)):
            ctk.CTkLabel(self.score_frame, text=self.yacht.players[i].name).grid(row=0, column=i+1, sticky=tk.W)
            ctk.CTkLabel(self.score_frame, text="0").grid(row=len(HANDS)+1, column=i+1, sticky=tk.W)
        for i in range(len(HANDS)):
            ctk.CTkLabel(self.score_frame, text=HANDS[i]).grid(row=i+1, column=0, sticky=tk.W)
            for j in range(len(self.yacht.players)):
                ctk.CTkButton(self.score_frame, text="   ", 
                              corner_radius=8, fg_color="gray",
                              font=("Permanent Marker", 20),
                          command=None,
                          width=130, height=40
                          ).grid(row=i+1, column=j+1, padx=1, pady=1)
        ctk.CTkLabel(self.score_frame, text="Sum: ").grid(row=len(HANDS)+1, column=0, sticky=tk.W)

        self.show_players_score()
        self.score_frame.pack()

        self.main_frame.pack()

    @property
    def yacht(self):
        return self.__yacht

    def update_dice_label(self):
        s = sorted(self.yacht.dice.copy())
        self.dice_label.configure(text=f"Dice: {s}")

    def show_players_score(self):
        dice = self.yacht.dice
        score = getScore(dice)
        for i in range(len(HANDS)):
            for j in range(len(self.yacht.players)):
                player = self.yacht.players[j]
                v = player.score[i]
                button = self.score_frame.grid_slaves(row=i+1, column=j+1)[0]

                if v is not None:
                    button.configure(text=str(v), state="disabled", fg_color="gray")
                elif self.yacht.current_player_idx == j:
                    if score[i] == 0:
                        button.configure(text="0", state="normal", 
                                     command=lambda i=i, j=j: self.yacht.setScore(j, i, 0), fg_color="gray")
                    else:
                        button.configure(text=score[i], state="normal", 
                                        command=lambda i=i, j=j: self.yacht.setScore(j, i, score[i]), fg_color="yellow")
                else:
                    button.configure(text="", state="disabled", fg_color="black")


if __name__ == "__main__":
    game = YachtGame(2)
    game.ui.mainloop()