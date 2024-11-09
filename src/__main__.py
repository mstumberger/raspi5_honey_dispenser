# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

from mstumb.honey_dispenser.config import Config
from mstumb.honey_dispenser.gui.main_window import Gui
from mstumb.honey_dispenser.scaling.dispenser import Dispenser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    Config.load_from_file('config.json')
    dispenser = Dispenser()
    gui = Gui(dispenser)
    gui.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/