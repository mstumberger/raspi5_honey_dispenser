from tk_tools import Gauge


# a subclass of Canvas for dealing with resizing of windows
class ResizingGauge(Gauge):

    def __init__(self, parent, width: int = 200, height: int = 100, min_value=0.0, max_value=100.0, label="", unit="",
                 divisions=8, yellow=50, red=80, yellow_low=0, red_low=0, bg="lightgrey"):
        super().__init__(parent, width, height, min_value, max_value, label, unit, divisions, yellow, red, yellow_low,
                         red_low, bg)
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self._width
        hscale = float(event.height)/self._height
        self._width = event.width
        self._height = event.height
        # resize the canvas
        self.config(width=self._width, height=self._height)
        # rescale all the objects tagged with the "all" tag
        self._canvas.scale("all", 0, 0, wscale, hscale)
