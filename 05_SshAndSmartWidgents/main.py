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


class AutoFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        '''Create all the widgets'''


class GraphicalEditor(AutoFrame):
    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Button-1>", print)
        self.canvas.bind("<ButtonRelease-1>", print)
        self.canvas.bind("<Motion>", print)
        self.canvas.grid(sticky="NEWS")

    def setTextEditor(self, text):
        self.textEditor = text


class TextEditor(AutoFrame):
    def create_widgets(self):
        self.text = tk.Text(self, undo=True)
        self.text.bind("<<Modified>>", print)
        self.text.grid(sticky="NEWS")

    def setGraphicalEditor(self, graph):
        self.graphicalEditor = graph


class Window(AutoFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.title("Ellipses")

    def create_widgets(self):
        graphFrame = GraphicalEditor(master=self)
        textFrame = TextEditor(master=self)
        textFrame.grid(row=0, column=0)
        graphFrame.grid(row=0, column=1)
        graphFrame.setTextEditor(textFrame)
        textFrame.setGraphicalEditor(graphFrame)


if __name__ == '__main__':
    app = Window(master=tk.Tk())
    app.mainloop()