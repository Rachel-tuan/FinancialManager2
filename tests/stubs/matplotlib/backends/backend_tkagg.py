class FigureCanvasTkAgg:
    def __init__(self, fig, master=None):
        self.fig = fig
    def get_tk_widget(self):
        return TkWidget()
    def draw(self): return None

class TkWidget:
    def pack(self, *a, **k): return None
