class GPIO:
    IN = None
    PUD_UP = None
    BOTH = None
    OUT = None
    BCM = None

    @staticmethod
    def setmode(arg):
        pass

    @staticmethod
    def setup(arg, arg1, pull_up_down=None):
        pass

    @staticmethod
    def output(arg, arg1):
        pass

    @staticmethod
    def add_event_detect(arg, arg1, callback=None):
        pass

    @staticmethod
    def input(arg):
        pass

    @staticmethod
    def cleanup():
        pass

    @classmethod
    def PWM(cls, SERVO_PIN, param):
        class PWM:
            def start(self, value=0):
                pass

        return PWM()


class Weight:
    def __init__(self, hx):
        self.hx = hx

    def getValue(self):
        return self.hx.current_weight

    # Define how to subtract two Weight objects
    def __sub__(self, other):
        if isinstance(other, Weight):
            return Weight(self.hx.current_weight - other.hx.current_weight)
        return NotImplemented

    # Define how to divide a Weight object by an int
    def __truediv__(self, other):
        if isinstance(other, int):  # Check if the divisor is an integer
            return Weight(self.hx / other)
        return NotImplemented

    # Define how to round a Weight object
    def __round__(self, n=0):
        return round(self.hx, n)

class SimpleHX711:
    def __init__(self, pin1, pin2, scale, factor, rate, dispenser=None):
        self.dispenser = dispenser
        self.current_weight = 0

    def setUnit(self, mass):
        pass

    def read(self, arg=0):
        return Weight(self)

    def weight(self, arg=0):
        if self.dispenser.lid_opened:
            self.current_weight += 50
        else:
            self.current_weight = 0
        return Weight(self)

    def setReferenceUnit(self, options):
        pass

    def setOffset(self, options):
        pass

    def zero(self, options):
        self.current_weight = 0

    # Define how to round a Weight object
    def __round__(self, n=0):
        return round(0, n)


class Rate:
    HZ_10 = 1


class Mass:
    class Unit:
        G=1


class Options:
    b = 3

    def __init__(self, arg=1, arg2=0):
        pass


class ReadType:
    Average = 4

