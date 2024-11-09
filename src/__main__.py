# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

from mstumb.honey_dispenser.config import Config
from mstumb.honey_dispenser.gui.main_window import Gui
from mstumb.honey_dispenser.scaling import Dispenser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Config.load_from_file('mstumb/honey_dispenser/config.json')
    dispenser = Dispenser(config, initial_weight=900, speed=0)
    gui = Gui(dispenser, config)
    gui.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/