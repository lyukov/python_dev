import tkinter as tk
import re


object_description = re.compile(
    r"(?P<type>oval) "
    r"\<"
    r"(?P<x0>[\d\.]+) "
    r"(?P<y0>[\d\.]+) "
    r"(?P<x1>[\d\.]+) "
    r"(?P<y1>[\d\.]+)"
    r"\> "
    r"(?P<thickness>[\d\.]+) "
    r"(?P<edge_color>#?\w+)"
    r"(?P<fill_color>#?\w+)"
)


class GraphicalEditor(tk.Frame):
    def __init__(self):
        pass

    def setTextEditor(self, text):
        self.textEditor = text


class TextEditor(tk.Frame):
    def __init__(self):
        pass

    def setGraphicalEditor(self, graph):
        self.graphicalEditor = graph


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Ellipses")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        graphFrame = GraphicalEditor(self)
        textFrame = TextEditor(self)
        graphFrame.setTextEditor(textFrame)
        textFrame.setGraphicalEditor(graphFrame)


if __name__ == '__main__':
    app = Window()
    app.mainloop()