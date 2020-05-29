"""
The main code for the game,
made by Leo Spratt please credit me
if you use this code elsewhere
"""

__version__ = "0.1.0"
__author__ = "Leo Spratt"

from collections import Counter
import pathlib
import tkinter as tk
from random import randint

SCRIPT_FILEPATH = pathlib.Path(__file__).parent.absolute()
app_config = {
    "CREDITS": 100,
    "GO_COST": 20,
    "LOAD_IMAGES_LOCAL": True,
    "IMAGE_SCALE": 4,
    "ASSETS": {
        "COMBINATIONS": "assets/combinations.gif",
        "BELL": "assets/bell.gif",
        "CHERRY": "assets/cherry.gif",
        "LEMON": "assets/lemon.gif",
        "ORANGE": "assets/orange.gif",
        "STAR": "assets/star.gif",
        "SKULL": "assets/skull.gif"
    }
}


class CreditsLabel(tk.Label):
    """
    used to allow easy access to update the credits display
    """
    def __init__(self, start_credits, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text=f"Credits: {start_credits}")

    def update_credits(self, newval):
        self.config(text=f"Credits: {newval}")


class GameReel:
    """
    The game reel class that
    contains each column for a row
    """
    __choices = (
        "BELL",
        "CHERRY",
        "LEMON",
        "ORANGE",
        "STAR",
        "SKULL"
    )
    def __init__(self):
        self.__reel = ["BELL", "BELL", "BELL"]

    def calc_row(self):
        """
        calculates the current row

        returns credits gained/loss or
        'GAMEOVER' if the game is over
        """
        counts = Counter(self.__reel).most_common(1)[0]
        if counts[1] == 1:
            return 0
        elif counts[0] == "SKULL":
            if counts[0][1] == 3:
                return "GAMEOVER"
            elif counts[0][1] == 2:
                return -100
        elif counts[0] == "BELL" and counts[1] == 3:
            return 500
        elif counts[1] == 3:
            return 100
        elif counts[1] == 2:
            return 50

    def spin(self):
        """
        spins the row
        """
        self.__reel = [
            self.__choices[randint(0, 5)],
            self.__choices[randint(0, 5)],
            self.__choices[randint(0, 5)]
        ]

    @property
    def reel(self):
        return self.__reel


class GameReels:
    """
    the game reels class that
    contains each row for the reel
    """
    def __init__(self):
        self.__reels = [GameReel() for i in range(3)]

    def calc_reels(self):
        """
        calculates all reels

        returns credits gained/loss or
        'GAMEOVER' if the game is over
        """
        credits_ = 0
        for reel in self.__reels:
            reel_value = reel.calc_row()
            if reel_value == "GAMEOVER":
                return "GAMEOVER"
            credits_ += reel_value
        return credits_

    def spin(self):
        """
        spins all the reels
        """
        for reel in self.__reels:
            reel.spin()

    @property
    def reels(self):
        return self.__reels

class ReelsFrame(tk.Frame):
    """
    The game reels in a tkinter frame
    """
    __game_reels = []
    def __init__(self, default_image: tk.PhotoImage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for row in range(0, 3):
            temp_col = []
            for col in range(0, 3):
                temp_col.append(tk.Label(self, image=default_image))
                temp_col[col].grid(row=row, column=col)
            self.__game_reels.append(temp_col)

    def set_image(self, row, column, new_image: tk.PhotoImage):
        """
        update a reel to have a new image
        """
        self.__game_reels[row][column].config(image=new_image)


class AppGui(tk.Tk):
    """
    The tkinter root window for the game
    """
    __app_config = app_config
    # __reels = []
    __images = {}
    __credits = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Fruit Machine " + self.app_version)
        self.__credits = self.__app_config["CREDITS"]

        self.__load_images()
        # self.__reels_frame = tk.Frame(self)
        # self.__load_reels()
        self.__reels_frame = ReelsFrame(self.__images["BELL"], self)
        self.__reels_frame.grid(row=0, column=0, columnspan=2)
        self.__l_combinations = tk.Label(self, image=self.__images["COMBINATIONS"])
        self.__l_combinations.grid(row=0, column=2)
        self.__l_credits = CreditsLabel(self.__credits, self)
        self.__l_credits.grid(row=1, column=0)
        self.__spin_bnt = tk.Button(self, text="Spin (costs 20)", command=self.spin)
        self.__spin_bnt.grid(row=1, column=1)

    def __load_reels(self):
        for row in range(0, 3):
            temp_col = []
            for col in range(0, 3):
                temp_label = tk.Label(self.__reels_frame)
                temp_label.config(image=self.__images["BELL"])
                temp_col.append(temp_label)
                temp_col[col].grid(row=row, column=col)
            self.__reels.append(temp_col)

    def spin(self):
        """
        called when the spin button is pressed
        """
        self.__credits -= 20
        self.__l_credits.update_credits(self.__credits)

    def __load_images(self):
        img_scale = self.__app_config["IMAGE_SCALE"]
        for key in self.__app_config["ASSETS"].keys():
            file_path = self.__app_config["ASSETS"][key]
            if self.__app_config["LOAD_IMAGES_LOCAL"] is True:
                file_path = pathlib.Path.joinpath(SCRIPT_FILEPATH, file_path)
            if key == "COMBINATIONS":
                self.__images["COMBINATIONS"] = tk.PhotoImage(file=file_path).zoom(2)
            else:
                self.__images[key] = tk.PhotoImage(file=file_path).zoom(img_scale)

    def load_config(self, new_config):
        self.__app_config = new_config

    @property
    def app_version(self):
        """returns the app __version__"""
        return __version__

if __name__ == "__main__":
    root = AppGui()
    root.mainloop()
