import tkinter as tk
import tkinter.colorchooser
import re
from enum import Enum


object_description = re.compile(
    r"^oval "
    r"\<"
    r"(?P<x0>\-?[\d\.]+) "
    r"(?P<y0>\-?[\d\.]+) "
    r"(?P<x1>\-?[\d\.]+) "
    r"(?P<y1>\-?[\d\.]+)"
    r"\> "
    r"(?P<width>[\d\.]+) "
    r"(?P<outline>#[\dA-Fa-f]{6}) "
    r"(?P<fill>#[\dA-Fa-f]{6})$"
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
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.rowconfigure(1, weight=0)
        self.__state = EditorState.FREE
        self.__object = None
        self.__coords = None
        self.__fill = "#55c600"
        self.__outline = "#000000"

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Button-1>", self.__onPress)
        self.canvas.bind("<ButtonRelease-1>", self.__onRelease)
        self.canvas.bind("<Motion>", self.__onMotion)
        self.canvas.grid(row=0, columnspan=3, sticky="NEWS")
        self.fillColorButton = tk.Button(self, text="Fill color", command=self.__newFillColor)
        self.fillColorButton.grid(row=1, column=0, sticky="NEWS")
        self.outlineColorButton = tk.Button(self, text="Outline color", command=self.__newOutlineColor)
        self.outlineColorButton.grid(row=1, column=1, sticky="NEWS")
        self.clearButton = tk.Button(self, text="Clear", command=self.__clear)
        self.clearButton.grid(row=1, column=2, sticky="NEWS")

    def setTextEditor(self, text):
        self.textEditor = text

    def __onPress(self, event):
        x, y = event.x, event.y
        self.__coords = x, y
        overlapping = self.canvas.find_overlapping(x, y, x, y)
        if overlapping:
            self.__state = EditorState.EDIT
            self.__object = overlapping[-1]
        else:
            self.__state = EditorState.NEW
            self.__object = self.canvas.create_oval(
                x, y, x, y,
                fill=self.__fill,
                outline=self.__outline
            )

    def __onMotion(self, event):
        if self.__state == EditorState.FREE:
            return
        elif self.__state == EditorState.NEW:
            self.canvas.coords(self.__object, *self.__coords, event.x, event.y)
        else:
            x0, y0 = self.__coords
            x, y = event.x, event.y
            self.canvas.move(self.__object, x - x0, y - y0)
            self.__coords = x, y

    def __onRelease(self, event):
        self.__state = EditorState.FREE
        self.__updateText()

    def __dumpObject(self, object):
        obj_type       = self.canvas.type(object)
        x0, y0, x1, y1 = self.canvas.coords(object)
        width          = self.canvas.itemcget(object, "width")
        outline        = self.canvas.itemcget(object, "outline")
        fill           = self.canvas.itemcget(object, "fill")
        return f"{obj_type} <{x0} {y0} {x1} {y1}> {width} {outline} {fill}"

    def __updateText(self):
        description = "\n".join(map(self.__dumpObject, self.canvas.find_all()))
        self.textEditor.text.delete("1.0", tk.END)
        self.textEditor.text.insert("1.0", description)

    def __newFillColor(self):
        self.__fill = tk.colorchooser.askcolor(color=self.__fill)[-1]

    def __newOutlineColor(self):
        self.__outline = tk.colorchooser.askcolor(color=self.__outline)[-1]

    def __clear(self):
        self.textEditor.text.delete("1.0", tk.END)


class TextEditor(AutoFrame):
    def create_widgets(self):
        self.text = tk.Text(self, undo=True)
        self.text.bind("<<Modified>>", self.__onModify)
        self.text.grid(sticky="NEWS")
        self.__WRONG_TAG = "wrong"
        self.text.tag_config(self.__WRONG_TAG, background="red")

    def setGraphicalEditor(self, graph):
        self.graphicalEditor = graph

    def __onModify(self, event):
        self.graphicalEditor.canvas.delete(tk.ALL)
        self.text.tag_remove(self.__WRONG_TAG, "1.0", tk.END)
        lines = self.text.get("1.0", tk.END).split("\n")
        for i, line in enumerate(lines):
            obj = object_description.match(line)
            if not obj:
                if line: self.text.tag_add(self.__WRONG_TAG, f"{i+1}.0", f"{i+1}.end")
                continue
            params = obj.groupdict()
            self.graphicalEditor.canvas.create_oval(
                params["x0"], params["y0"], params["x1"], params["y1"],
                width=params["width"],
                outline=params["outline"],
                fill=params["fill"]
            )
        self.text.edit_modified(False)


class Window(AutoFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.title("Ellipses")
        self.columnconfigure(1, weight=4)

    def create_widgets(self):
        self.graphFrame = GraphicalEditor(master=self)
        self.textFrame = TextEditor(master=self)
        self.textFrame.grid(row=0, column=0, sticky="NEWS")
        self.graphFrame.grid(row=0, column=1, sticky="NEWS")
        self.graphFrame.setTextEditor(self.textFrame)
        self.textFrame.setGraphicalEditor(self.graphFrame)


if __name__ == '__main__':
    app = Window(master=tk.Tk())
    app.mainloop()