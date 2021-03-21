import tkinter as tk
from functools import partial
from tkinter.messagebox import showinfo


DEFAULT_GRAVITY = "NEWS"


def embedNewWidget(parent, name, widget_type, geometry, **kwargs):
    class NewWidget(widget_type):
        def __init__(self, geometry, **kwargs):
            super().__init__(**kwargs)
            self.__set_geometry(geometry)

        def __set_geometry(self, geometry):

            def parse(geometry_str, delimiter, default_value):
                res = geometry_str.split(delimiter)
                ans = default_value if len(res) < 2 else res[1]
                return res[0], ans

            def parse_row_col_geometry(geometry):
                geometry, span = parse(geometry, '+', 0)
                num, weight = parse(geometry, '.', 1)
                return int(num), int(weight), int(span)

            geometry, gravity = parse(geometry, '/', DEFAULT_GRAVITY)
            row_params, col_params = geometry.split(':')
            row, row_weight, height = parse_row_col_geometry(row_params)
            col, col_weight, width  = parse_row_col_geometry(col_params)

            self.grid(
                row=row,
                rowspan=height + 1,
                column=col,
                columnspan=width + 1,
                sticky=gravity
            )
            self.master.rowconfigure(row, weight=row_weight)
            self.master.columnconfigure(col, weight=col_weight)

        def __getattr__(self, item):
            return partial(embedNewWidget, self, item)

    widget = NewWidget(geometry, master=parent, **kwargs)
    setattr(parent, name, widget)
    return widget


class Application(tk.Frame):
    def __init__(self, title):
        super().__init__()
        self.master.title(title)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(sticky=DEFAULT_GRAVITY)
        self.createWidgets()

    def createWidgets(self):
        pass

    def __getattr__(self, item):
        return partial(embedNewWidget, self, item)


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()