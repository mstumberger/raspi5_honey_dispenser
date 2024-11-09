import unittest

from mstumb.honey_dispenser.config import Config
from mstumb.honey_dispenser.scaling.dispenser import Dispenser

Config.load_from_file('config.json')


class TestStepper(unittest.TestCase):
    dispenser = Dispenser(speed=0)

    def test_upper(self):
        self.assertEqual(0, self.dispenser.current_step)
        self.dispenser.open_lid()
        self.assertEqual(self.dispenser.max_steps, self.dispenser.current_step)
        self.dispenser.rotate_stepper(6)
        self.assertEqual(self.dispenser.max_steps + 6, self.dispenser.current_step)
        self.dispenser.check_weight(600)
        self.assertEqual(4, self.dispenser.current_step)
        self.dispenser.check_weight(801)
        self.assertEqual(0, self.dispenser.current_step)


if __name__ == '__main__':
    unittest.main()