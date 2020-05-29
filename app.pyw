"""
The main code for the game,
made by Leo Spratt please credit me
if you use this code elsewhere
"""

__version__ = "0.1.0"
__author__ = "Leo Spratt"

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

class AppGui(tk.Tk):
    """
    The tkinter root window for the game
    """
    __app_config = app_config
    __reels = []
    __images = {}
    __credits = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Fruit Machine " + self.app_version)
        self.__credits = self.__app_config["CREDITS"]

        self.__load_images()
        self.__reels_frame = tk.Frame(self)
        self.__load_reels()
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
