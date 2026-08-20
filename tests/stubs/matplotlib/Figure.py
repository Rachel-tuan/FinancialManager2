class Figure:
    def __init__(self, figsize=None, dpi=None):
        self.figsize = figsize
        self.dpi = dpi
    def add_subplot(self, *a):
        return Axes()
    def set_figheight(self, *a): return None
    def set_figwidth(self, *a): return None
    def tight_layout(self, *a): return None
    def savefig(self, *a, **k): return None

class Axes:
    def clear(self): return None
    def barh(self, *a, **k):
        return [Bar()]
    def text(self, *a, **k): return None
    def set_title(self, *a, **k): return None
    def set_xlabel(self, *a, **k): return None
    def tick_params(self, *a, **k): return None
    def get_yticklabels(self): return [Label()]
    def get_width(self): return 10

class Bar:
    def get_width(self): return 10
    def get_y(self): return 0
    def get_height(self): return 1

class Label:
    def set_fontfamily(self, *a): return None
