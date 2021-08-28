"""
the gui
"""
__all__ = ["ValueLabel", "ReelsFrame", "AppGui"]

import tkinter as tk
from tkinter.messagebox import showinfo

from . import __version__
from .reel import GameReels
from .types import AppSettings, IconNames


class ValueLabel(tk.Label):
    """
    used to allow easy access to update the credits display
    """
    def __init__(self, start_value, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__text = text
        self.value = start_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newval):
        self.__value = newval
        self.config(text=f"{self.__text}: {newval}")


class ReelsFrame(tk.Frame):
    """
    The game reels in a tkinter frame
    """
    __game_reels = []
    def __init__(self, default_image: tk.PhotoImage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__load_reel_images(default_image)

    def __setup_reel_image_col(self, image: tk.PhotoImage, row: int, col: int):
        """
        setup a reel column image

            :param image: the image to use
            :param row: the current row
            :param col: the current column
            :return: the label
        """
        reel_column = tk.Label(self, image=image)
        reel_column.grid(row=row, column=col)
        return reel_column

    def __load_reel_images(self, image: tk.PhotoImage):
        """
        add reel images into frame

            :param image: the image to load into game reels
        """
        for row in range(3):
            temp_col = []
            for col in range(3):
                temp_col.append(self.__setup_reel_image_col(image, row, col))
            self.__game_reels.append(temp_col)

    def set_image(self, row, column, new_image: tk.PhotoImage):
        """
        update a reel to have a new image
        """
        self.__game_reels[row][column].config(image=new_image)


class AppGui(tk.Tk):
    """
    The tkinter root window for the game

        :param app_config: the app config
    """
    __images = {}
    __credits = 0
    def __init__(self, app_config: AppSettings, **kwargs):
        super().__init__(**kwargs)
        self.__app_config = app_config
        self.title("Fruit Machine " + self.app_version)
        self.__credits = self.__app_config.starting_credits
        self.__reels = GameReels()

        self.__load_images()
        self.__reels_frame = ReelsFrame(self.__images[IconNames.BELL], self)
        self.__reels_frame.grid(row=0, column=0, columnspan=2)
        self.__l_combinations = tk.Label(self, image=self.__images[IconNames.COMBINATIONS])
        self.__l_combinations.grid(row=0, column=2)
        self.__l_curr_winnings = ValueLabel(0, "Current Winnings", self)
        self.__l_curr_winnings.grid(row=1, column=0)
        self.__l_credits = ValueLabel(self.__credits, "Credits", self)
        self.__l_credits.grid(row=2, column=0)
        self.__spin_bnt = tk.Button(
            self,
            text=f"Spin (costs {self.__app_config.go_cost})",
            command=self.spin
        )
        self.__spin_bnt.grid(row=1, column=1)

    def load_reel_images(self):
        """
        loads reel images from the current spin of reels
        """
        for row, reel_row in enumerate(self.__reels.reels):
            for col, reel_col in enumerate(reel_row.reel):
                self.__reels_frame.set_image(
                    row, col,
                    self.__images.get(reel_col)
                )

    def reset_game(self):
        """
        resets the credits
        """
        self.__credits = self.__app_config.starting_credits
        self.__l_curr_winnings.value = 0
        self.__l_credits.value = self.__credits
        self.__reels.to_default()
        self.load_reel_images()

    def spin(self):
        """
        called when the spin button is pressed
        """
        self.__credits -= self.__app_config.go_cost
        self.__l_credits.value = self.__credits
        self.__reels.spin()
        self.load_reel_images()
        credits_won = self.__reels.calc_reels()
        if credits_won == "GAMEOVER":
            showinfo(title="Game Over", message="You got 3 skulls")
            self.reset_game()
        else:
            temp_credits = self.__credits
            temp_credits += credits_won
            self.__credits = temp_credits
            self.__l_credits.value = self.__credits
            self.__l_curr_winnings.value = credits_won
            if temp_credits < 0:
                showinfo(title="Game Over", message="You have lost all of your credits!!!")
                self.reset_game()

    def __load_images(self):
        """
        adds the game assets from file to tk.PhotoImage
        """
        img_scale = self.__app_config.image_scale
        for key in self.__app_config.assets:
            file_path = self.__app_config.assets[key]
            if key == IconNames.COMBINATIONS:
                self.__images[IconNames.COMBINATIONS] = tk.PhotoImage(file=file_path).zoom(2)
            else:
                self.__images[key] = tk.PhotoImage(file=file_path).zoom(img_scale)

    def load_config(self, new_config):
        """
        loads a new config,
        overwriting the old one
        """
        self.__app_config = new_config

    @property
    def app_version(self):
        """
        returns the app __version__
        """
        return __version__
