"""tkinter 桩：模拟 Tk 控件行为，供无显示环境下的 UI 冒烟测试。"""

END = 'end'


class FakeWidget:
    def __init__(self, *a, **k):
        self._v = k.get('textvariable', None)
        pass
    def pack(self, *a, **k): return None
    def pack_propagate(self, *a, **k): return None
    def grid(self, *a, **k): return None
    def configure(self, *a, **k): return None
    config = configure
    def set(self, *a, **k): return None
    def get(self, *a, **k): return None
    def delete(self, *a, **k): return None
    def insert(self, *a, **k): return None
    def heading(self, *a, **k): return None
    def column(self, *a, **k): return None
    def item(self, *a, **k): return None
    def tag_configure(self, *a, **k): return None
    def get_children(self): return []
    def create_window(self, *a, **k): return None
    def get_tk_widget(self): return self
    def draw(self): return None
    def update_idletasks(self): return None
    def bbox(self, *a): return (0, 0, 100, 100)
    def xview_scroll(self, *a): return None
    def yview_scroll(self, *a): return None
    def xview(self, *a): return None
    def yview(self, *a): return None
    def bind_all(self, *a): return None
    def focus_set(self): return None
    def destroy(self): return None
    def grab_set(self): return None
    def transient(self, *a): return None
    def resizable(self, *a): return None
    def geometry(self, *a): return None
    def title(self, *a): return None
    def clear(self): return None
    def text(self, *a, **k): return None
    def set_title(self, *a, **k): return None
    def set_xlabel(self, *a, **k): return None
    def tick_params(self, *a, **k): return None
    def get_yticklabels(self): return []
    def savefig(self, *a, **k): return None
    def add_subplot(self, *a): return FakeWidget()
    def set_figheight(self, *a): return None
    def set_figwidth(self, *a): return None
    def tight_layout(self, *a): return None
    def mainloop(self): return None


class StringVar(FakeWidget):
    def __init__(self, value=''):
        self._v = value
    def get(self):
        return self._v
    def set(self, value):
        self._v = value


class Tk(FakeWidget):
    pass


class Toplevel(FakeWidget):
    pass


class Frame(FakeWidget):
    pass


class LabelFrame(FakeWidget):
    pass


class Label(FakeWidget):
    pass


class Entry(FakeWidget):
    pass


class Button(FakeWidget):
    pass


class Canvas(FakeWidget):
    pass


class Text(FakeWidget):
    pass


class Combobox(FakeWidget):
    pass


class Style(FakeWidget):
    def theme_use(self, *a): return None
    def map(self, *a, **k): return None


class Treeview(FakeWidget):
    pass


class Scrollbar(FakeWidget):
    pass


class messagebox:
    showwarning = staticmethod(lambda *a, **k: None)
    showinfo = staticmethod(lambda *a, **k: None)
    showerror = staticmethod(lambda *a, **k: None)


class filedialog:
    asksaveasfilename = staticmethod(lambda *a, **k: None)


class font:
    pass


class _Ttk:
    Combobox = Combobox
    Style = Style
    Treeview = Treeview
    Scrollbar = Scrollbar


ttk = _Ttk()