import os
import sys
from .. import __version__
from ..exceptions import (LoosingReelException, NoCreditsException,
                          NotEnoughCreditsException)
from ..game import Game
from ..types import AppSettings, IconNames

ICON_NAMES_TITLE = {
    IconNames.BELL: "BELL",
    IconNames.CHERRY: "CHERRY",
    IconNames.LEMON: "LEMON",
    IconNames.ORANGE: "ORANGE",
    IconNames.STAR: "STAR",
    IconNames.SKULL: "SKULL",
}

class AppCli:
    def __init__(self, app_config: AppSettings) -> None:
        self.__app_config = app_config
        self.__title = "Fruit Machine " + self.app_version
        self.__game = Game(
            self.__app_config.starting_credits,
            self.__app_config.go_cost,
        )

    @staticmethod
    def clear_console():
        os.system("cls" if os.name in ("nt", "dos") else "clear")

    def output_stats(self):
        print("Stats:")
        print(
            f"Last Spin = {self.__game.credits_won},",
            f"Credits = {self.__game.curr_credits}"
        )

    def output_reels(self):
        print("---")
        for reel_row in self.__game.reels:
            titles = [ICON_NAMES_TITLE[col] for col in reel_row.reel]
            print("\t|".join(titles))
        print("---")

    def show_spin(self):
        self.clear_console()
        print(self.__title)
        self.output_stats()
        print("Spin:")

        try:
            self.__game.spin()
            self.output_reels()
            self.__game.calc_spin()

        except NotEnoughCreditsException:
            print("You don't have enough credits to spin!")

        except NoCreditsException:
            print("You have lost all of your credits!")

        except LoosingReelException:
            print("You got 3 skulls!")

        input("(press <enter> to resume)")

    def show_menu(self):
        self.clear_console()
        print(self.__title)
        self.output_stats()
        print("Menu:")
        print(f"\t1. Spin (costs {self.__app_config.go_cost})")
        print("\t2. Restart")
        print("\t3. Quit")

        choice = input(">> ")

        if choice == "1":
            self.show_spin()
        elif choice == "2":
            self.__game.reset()
        elif choice == "3":
            sys.exit()
        else:
            print(f"unknown choice: '{choice}'")
            input("(press <enter> to resume)")

    def start(self):
        try:
            while True:
                self.show_menu()
        except KeyboardInterrupt:
            sys.exit()

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
