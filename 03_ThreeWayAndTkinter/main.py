import tkinter as tk
import random

def immutableShuffle(x):
    return random.sample(x, len(x))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='NEWS')
        self.createWidgets()
        self.flexibleItems()

    def createWidgets(self):
        self.newButton = tk.Button(self, text='New', command=self.newGame)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit)
        self.tiles = [tk.Button(self, text=str(i), command=self.step) for i in range(1, 16)]
        self.newButton.grid(row=0, column=0, columnspan=2, sticky='NEWS')
        self.exitButton.grid(row=0, column=2, columnspan=2, sticky='NEWS')
        self.newGame()

    def flexibleItems(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(4):
            self.columnconfigure(col, weight=1)

    def newGame(self):
        for i, tile in enumerate(immutableShuffle(self.tiles)):
            tile.grid(row = i // 4 + 1, column = i % 4, sticky='NEWS')

    def step(self):
        pass

app = Application()
app.master.title('15')
app.mainloop()
