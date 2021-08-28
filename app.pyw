"""
Python Fruit Machine
Copyright (C) 2018  {Leo Spratt}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = "0.3.0"
__author__ = "Leo Spratt"

import enum
import pathlib
import random
import tkinter as tk
from collections import Counter
from dataclasses import dataclass
from tkinter.messagebox import showinfo

SCRIPT_FILEPATH = pathlib.Path(__file__).parent.absolute()


@enum.unique
class IconNames(enum.IntEnum):
    """
    Enums for Icon Names
    """
    COMBINATIONS = enum.auto()
    SKULL = enum.auto()
    BELL = enum.auto()
    CHERRY = enum.auto()
    LEMON = enum.auto()
    ORANGE = enum.auto()
    STAR = enum.auto()


@dataclass
class AppSettings:
    """
    Holds the app settings
    """
    starting_credits: int
    go_cost: int
    load_images_local: bool
    image_scale: int
    assets: dict


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


class GameReel:
    """
    The game reel class that
    contains each column for a row
    """
    __choices = (
        IconNames.BELL,
        IconNames.CHERRY,
        IconNames.LEMON,
        IconNames.ORANGE,
        IconNames.STAR,
        IconNames.SKULL
    )
    __weights = (1, 3, 3, 3, 3, 5)
    def __init__(self):
        self.__reel = [IconNames.BELL, IconNames.BELL, IconNames.BELL]

    def calc_row(self):
        """
        calculates the current row

        returns credits gained/loss or
        'GAMEOVER' if the game is over
        """
        counts = Counter(self.__reel).most_common(1)[0]
        if counts[1] == 1:
            return 0
        elif counts[0] == IconNames.SKULL:
            if counts[1] == 3:
                return "GAMEOVER"
            elif counts[1] == 2:
                return -100
        elif counts[0] == IconNames.BELL and counts[1] == 3:
            return 500
        elif counts[1] == 3:
            return 100
        elif counts[1] == 2:
            return 50

    def __spin_reel_col(self):
        return random.choices(self.__choices, self.__weights)[0]

    def spin(self):
        """
        spins the row, using choices and
        weights for randomly picking
        """
        self.__reel = [
            self.__spin_reel_col(),
            self.__spin_reel_col(),
            self.__spin_reel_col()
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

    def to_default(self):
        """
        reset the reels to default values
        """
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

        :param app_config: dict of the app config
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
        curr_reels = self.__reels.reels
        for row in range(len(curr_reels)):
            for col in range(len(curr_reels[row].reel)):
                self.__reels_frame.set_image(
                    row, col,
                    self.__images.get(curr_reels[row].reel[col])
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
                showinfo(title="Game Over", message="You have gone into negative credits")
                self.reset_game()

    def __load_images(self):
        """
        adds the game assets from file to tk.PhotoImage
        """
        img_scale = self.__app_config.image_scale
        for key in self.__app_config.assets.keys():
            file_path = self.__app_config.assets[key]
            if self.__app_config.load_images_local is True:
                file_path = pathlib.Path.joinpath(SCRIPT_FILEPATH, file_path)
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


def main():
    app_config = AppSettings(
        starting_credits=100,
        go_cost=20,
        load_images_local=True,
        image_scale=4,
        assets={
            IconNames.COMBINATIONS: "assets/combinations.gif",
            IconNames.BELL: "assets/bell.gif",
            IconNames.CHERRY: "assets/cherry.gif",
            IconNames.LEMON: "assets/lemon.gif",
            IconNames.ORANGE: "assets/orange.gif",
            IconNames.STAR: "assets/star.gif",
            IconNames.SKULL: "assets/skull.gif"
        },
    )
    root = AppGui(app_config)
    root.mainloop()

if __name__ == "__main__":
    main()
