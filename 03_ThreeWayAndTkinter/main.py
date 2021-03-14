import tkinter as tk
import random

EMPTY = -1

def immutableShuffle(x):
    return random.sample(x, len(x))

class Tile(tk.Button):
    def __init__(self, master, number, gameGrid):
        super().__init__(master, text=str(number), command=self.makeStep)
        self.number = number
        self.position = (-1, -1)
        self.gameGrid = gameGrid

    def setPosition(self, position):
        row, col = position // 4, position % 4
        self.grid(row=row+1, column=col, sticky='NEWS')
        self.position = position
        self.gameGrid[position] = self.number

    def makeStep(self):
        for direction in [-4, 4, -1, 1]:
            newPosition = self.position + direction
            if 0 <= newPosition < 16 and self.gameGrid[newPosition] == EMPTY:
                self.gameGrid[self.position] = EMPTY
                self.setPosition(newPosition)
                return

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='NEWS')
        self.gameGrid = [EMPTY for i in range(16)]
        self.createWidgets()
        self.flexibleItems()

    def createWidgets(self):
        self.newButton = tk.Button(self, text='New', command=self.newGame)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit)
        self.tileNums = list(range(1, 16))
        self.tiles = [Tile(self, i, self.gameGrid) for i in self.tileNums]
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
        shuffledNums = immutableShuffle(self.tileNums)
        for i, num in enumerate(shuffledNums):
            self.tiles[num - 1].setPosition(i)


app = Application()
app.master.title('15')
app.mainloop()
