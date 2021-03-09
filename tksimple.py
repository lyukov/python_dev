import time
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self._counter = 0
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.button_1 = tk.Button(self, text='+1', command=self.inc1)
        self.button_10 = tk.Button(self, text='+10', command=self.inc10)
        self.button_100 = tk.Button(self, text='+100', command=self.inc100)
        self.button_square = tk.Button(self, text='Square', command=self.square)
        self.counter_label = tk.Label(self)
        self.button_1.grid(row=0, column=0)
        self.button_10.grid(row=0, column=1)
        self.button_100.grid(row=0, column=2)
        self.button_square.grid(row=0, column=3)
        self.quitButton.grid(columnspan=4)
        self.counter_label.grid(columnspan=4)
        self.updateText()

    def inc1(self):
        self._counter += 1
        self.updateText()

    def inc10(self):
        self._counter += 10
        self.updateText()

    def inc100(self):
        self._counter += 100
        self.updateText()

    def square(self):
        self._counter *= self._counter
        self.updateText()

    def updateText(self):
        self.counter_label["text"] = str(self._counter)

app = Application()
app.master.title('Clicker')
app.mainloop()
