import tkinter as tk
import tkinter.messagebox
import random

EMPTY = -1
N = 4

def immutableShuffle(x):
    return random.sample(x, len(x))

class Tile(tk.Button):
    def __init__(self, master, number, gameGrid, winState):
        super().__init__(
            master,
            text=str(number),
            command=self.makeStep,
            width=2
        )
        self.number = number
        self.position = (-1, -1)
        self.gameGrid = gameGrid
        self.winState = winState
        self.app = master

    def setPosition(self, position):
        row, col = position // N, position % N
        self.grid(row=row+1, column=col, sticky='NEWS')
        self.position = position
        self.gameGrid[position] = self.number

    def makeStep(self):
        for direction in [-N, N, -1, 1]:
            newPosition = self.position + direction
            if 0 <= newPosition < N*N and self.gameGrid[newPosition] == EMPTY:
                self.gameGrid[self.position] = EMPTY
                self.setPosition(newPosition)
                self.checkWin()
                return

    def checkWin(self):
        if self.gameGrid == self.winState:
            tkinter.messagebox.showinfo('', 'Congratulations! You win!')
            self.app.newGame()

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='NEWS')
        self.gameGrid = [EMPTY for i in range(N * N)]
        self.winState = list(range(1, N * N)) + [EMPTY]
        self.createWidgets()
        self.flexibleItems()

    def createWidgets(self):
        self.newButton = tk.Button(self, text='New', command=self.newGame)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit)
        self.tileNums = list(range(1, N * N))
        self.tiles = [Tile(self, i, self.gameGrid, self.winState) for i in self.tileNums]
        self.newButton.grid(row=0, column=0, columnspan=N // 2, sticky='NEWS')
        self.exitButton.grid(row=0, column=N // 2, columnspan=N - N // 2, sticky='NEWS')
        self.newGame()

    def flexibleItems(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for row in range(N + 1):
            self.rowconfigure(row, weight=1)
        for col in range(N):
            self.columnconfigure(col, weight=1)

    def newGame(self):
        shuffledNums = immutableShuffle(self.tileNums)
        for i, num in enumerate(shuffledNums):
            self.tiles[num - 1].setPosition(i)
        self.gameGrid[-1] = EMPTY

if __name__=='__main__':
    app = Application()
    app.master.title(str(N * N - 1))
    app.mainloop()
