import tkinter as tk
import re
from enum import Enum


object_description = re.compile(
    r"(?P<type>oval) "
    r"\<"
    r"(?P<x0>[\d\.]+) "
    r"(?P<y0>[\d\.]+) "
    r"(?P<x1>[\d\.]+) "
    r"(?P<y1>[\d\.]+)"
    r"\> "
    r"(?P<width>[\d\.]+) "
    r"(?P<outline>#?\w+)"
    r"(?P<fill>#?\w+)"
)


class EditorState(Enum):
    FREE = 1
    NEW  = 2
    EDIT = 3


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
        self.canvas.bind("<Button-1>", self.onPress)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<Motion>", self.onMotion)
        self.canvas.grid(sticky="NEWS")
        self.state = EditorState.FREE
        self.object = None
        self.coords = None
        self.fill = "#000000"
        self.outline = "#FFFFFF"

    def setTextEditor(self, text):
        self.textEditor = text

    def onPress(self, event):
        x, y = event.x, event.y
        self.coords = x, y
        overlapping = self.canvas.find_overlapping(x, y, x, y)
        if overlapping:
            self.state = EditorState.EDIT
            self.object = overlapping[-1]
        else:
            self.state = EditorState.NEW
            self.object = self.canvas.create_oval(
                x, y, x, y,
                fill=self.fill,
                outline=self.outline
            )

    def onMotion(self, event):
        if self.state == EditorState.FREE:
            return
        elif self.state == EditorState.NEW:
            self.canvas.coords(self.object, *self.coords, event.x, event.y)
        else:
            x0, y0 = self.coords
            x, y = event.x, event.y
            self.canvas.move(self.object, x - x0, y - y0)
            self.coords = x, y

    def onRelease(self, event):
        self.state = EditorState.FREE
        self.updateText()

    def dumpObject(self, object):
        obj_type       = self.canvas.type(object)
        x0, y0, x1, y1 = self.canvas.coords(object)
        width          = self.canvas.itemcget(object, "width")
        outline        = self.canvas.itemcget(object, "outline")
        fill           = self.canvas.itemcget(object, "fill")
        return f"{obj_type} <{x0} {y0} {x1} {y1}> {width} {outline} {fill}"

    def updateText(self):
        description = "\n".join(map(self.dumpObject, self.canvas.find_all()))
        self.textEditor.text.delete("1.0", tk.END)
        self.textEditor.text.insert("1.0", description)


class TextEditor(AutoFrame):
    def create_widgets(self):
        self.text = tk.Text(self, undo=True)
        self.text.bind("<<Modified>>", self.onModify)
        self.text.grid(sticky="NEWS")

    def setGraphicalEditor(self, graph):
        self.graphicalEditor = graph

    def onModify(self, event):
        print(event)


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