from pathlib import Path

from fruit_machine.gui import AppGui
from fruit_machine.types import AppSettings, IconNames

ASSETS_FILEPATH = Path(__file__).parent.absolute() / "assets"
DEFAULT_ASSET_PATHS = {
    IconNames.COMBINATIONS: ASSETS_FILEPATH / "combinations.gif",
    IconNames.BELL: ASSETS_FILEPATH / "bell.gif",
    IconNames.CHERRY: ASSETS_FILEPATH / "cherry.gif",
    IconNames.LEMON: ASSETS_FILEPATH / "lemon.gif",
    IconNames.ORANGE: ASSETS_FILEPATH / "orange.gif",
    IconNames.STAR: ASSETS_FILEPATH / "star.gif",
    IconNames.SKULL: ASSETS_FILEPATH / "skull.gif"
}


def main():
    """
    main entry point of the app
    """
    app_config = AppSettings(
        starting_credits=100,
        go_cost=20,
        image_scale=4,
        assets=DEFAULT_ASSET_PATHS,
    )
    root = AppGui(app_config)
    root.mainloop()

if __name__ == "__main__":
    main()
