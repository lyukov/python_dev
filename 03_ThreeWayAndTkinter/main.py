import tkinter as tk
import random

def immutableShuffle(x):
    return random.sample(x, len(x))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.newButton = tk.Button(self, text='New', command=self.newGame)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit)
        self.tiles = [tk.Button(self, text=str(i), command=self.step) for i in range(1, 16)]
        self.newButton.grid(row=0, column=0)
        self.exitButton.grid(row=0, column=2)
        self.newGame()

    def newGame(self):
        for i, tile in enumerate(immutableShuffle(self.tiles)):
            tile.grid(row = i // 4 + 1, column = i % 4)

    def step(self):
        pass

app = Application()
app.master.title('15')
app.mainloop()
