import random
import tkinter
from tkinter import Tk, Canvas, Frame, ALL, Button, Label, LEFT, RIGHT, NW, NE , BOTH, Y, X


class Cons:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 100
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27


class Board(Frame):
    def __init__(self):
        super().__init__()
        self.master.title('Cube')

        controls_frame = Frame(background='pink', width=100)
        controls_frame.pack(fill=Y,anchor=NW)
        graphic_frame = Frame(bg='red', width=100)
        graphic_frame.pack(fill=BOTH,anchor=NE)
        self.cube = RubiksCube(graphic_frame)

        x_Frame = Frame(controls_frame, background="green", width=100, height=100)
        y_Frame = Frame(controls_frame, background="green", width=100, height=100)
        z_Frame = Frame(controls_frame, background="green", width=100, height=100)
        x_Frame.pack(anchor=NE,side=LEFT)
        y_Frame.pack(anchor=NE,side=LEFT)
        z_Frame.pack(anchor=NE,side=LEFT)
        Button(x_Frame,text="x1_up", command=self.x1_up).pack()
        Button(x_Frame,text="x1_down", command=self.x1_down).pack()
        Button(x_Frame,text="x2_up", command=self.x2_up).pack()
        Button(x_Frame,text="x2_down", command=self.x2_down).pack()
        Button(x_Frame,text="x3_up", command=self.x3_up).pack()
        Button(x_Frame,text="x3_down", command=self.x3_down).pack()
        Button(y_Frame,text="y1_right", command=self.y1_right).pack()
        Button(y_Frame,text="y1_left", command=self.y1_left).pack()
        Button(y_Frame,text="y2_right", command=self.y2_right).pack()
        Button(y_Frame,text="y2_left", command=self.y2_left).pack()
        Button(y_Frame,text="y3_right", command=self.y3_right).pack()
        Button(y_Frame,text="y3_left", command=self.y3_left).pack()
        Button(z_Frame,text="z1_up", command=self.z1_up).pack()
        Button(z_Frame,text="z1_down", command=self.z1_down).pack()
        Button(z_Frame,text="z2_up", command=self.z2_up).pack()
        Button(z_Frame,text="z2_down", command=self.z2_down).pack()
        Button(z_Frame,text="z3_up", command=self.z3_up).pack()
        Button(z_Frame,text="z3_down", command=self.z3_down).pack()
        self.pack()

    def x1_up(self): self.cube.rotate(1)
    def x1_down(self): self.cube.rotate(2)
    def x2_up(self): self.cube.rotate(3)
    def x2_down(self): self.cube.rotate(4)
    def x3_up(self): self.cube.rotate(5)
    def x3_down(self): self.cube.rotate(6)
    def y1_right(self): self.cube.rotate(7)
    def y1_left(self): self.cube.rotate(8)
    def y2_right(self): self.cube.rotate(9)
    def y2_left(self): self.cube.rotate(10)
    def y3_right(self): self.cube.rotate(11)
    def y3_left(self): self.cube.rotate(12)
    def z1_up(self): self.cube.rotate(13)
    def z1_down(self): self.cube.rotate(14)
    def z2_up(self): self.cube.rotate(15)
    def z2_down(self): self.cube.rotate(16)
    def z3_up(self): self.cube.rotate(17)
    def z3_down(self): self.cube.rotate(18)


class RubiksCube(Canvas):
    def __init__(self, graphic_frame):
        super().__init__(graphic_frame)#width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT, highlightthickness=0, background="gray")
        self.initCube()
        self.pack(anchor=NW, side=RIGHT)

    def initCube(self):
        self.margin = 20
        self.edgeLen = 20
        self.colors = ['blue', 'yellow', 'red', 'white', 'orange', 'green']
        self.matrix = [[y + x * 9 for y in range(0, 9)] for x in range(6)]
        # двумерный [лево, верх, фронт, низ, спина, право]
        self.colors = [self.colors[x // 9] for x in range(54)]
        self.offset = ((0, 3 * self.edgeLen),
                       (3 * self.edgeLen, 0),
                       (3 * self.edgeLen, 3 * self.edgeLen),
                       (3 * self.edgeLen, 6 * self.edgeLen),
                       (3 * self.edgeLen, 9 * self.edgeLen),
                       (6 * self.edgeLen, 3 * self.edgeLen))

        self.after(Cons.DELAY, self.printCube)

    def printCube(self):
        self.delete(ALL)
        for facetInd in range(len(self.matrix)):
            for squareInd in range(9):
                offset = self.offset[facetInd]
                shift = squareInd // 3
                bbox = (self.margin+offset[0] + self.edgeLen * squareInd - self.edgeLen * 3 * shift,
                        self.margin+offset[1] + self.edgeLen * shift,
                        self.margin+offset[0] + self.edgeLen * squareInd + self.edgeLen - self.edgeLen * 3 * shift,
                        self.margin+offset[1] + self.edgeLen * shift + self.edgeLen)
                # верхнего левого и правого нижнего угла
                # x0, y0, x1, y1
                self.create_rectangle(*bbox, fill=self.colors[self.matrix[facetInd][squareInd]], activefill="black")
        self.after(Cons.DELAY, self.printCube)

    def rotate(self, move):
        if move == 1:  # x1 up and side 0 counterclockwise
            self.verticalMove(0, True)
            self.rotateSaide(0, False)
        elif move == 2:  # x1 down and side 0 clockwise
            self.verticalMove(0, False)
            self.rotateSaide(0, True)
        elif move == 3:  # x2 up
            self.verticalMove(1, True)
        elif move == 4:  # x2 down
            self.verticalMove(1, False)
        elif move == 5:  # x3 up and side 5 clockwise
            self.verticalMove(2, True)
            self.rotateSaide(5, True)
        elif move == 6:  # x3 down and side 5 counterclockwise
            self.verticalMove(2, False)
            self.rotateSaide(5, False)
        elif move == 7:  # y1 right and side 3 clockwise
            self.horisontalMove(6, True)
            self.rotateSaide(3, True)
        elif move == 8:  # y1 left and side 3 counterclockwise
            self.horisontalMove(6, False)
            self.rotateSaide(3, False)
        elif move == 9:  # y2 right
            self.horisontalMove(3, True)
        elif move == 10:  # y2 left
            self.horisontalMove(3, False)
        elif move == 11:  # y3 right and side 1 counterclockwise
            self.horisontalMove(0, True)
            self.rotateSaide(1, False)
        elif move == 12:  # y3 left and side 1 clockwise
            self.horisontalMove(0, False)
            self.rotateSaide(1, True)
        elif move == 13:  # z1 up and side 2 clockwise
            self.z_verticalMove(0, True)
            self.rotateSaide(2, True)
        elif move == 14:  # z1 down and side 2 counterclockwise
            self.z_verticalMove(0, False)
            self.rotateSaide(2, False)
        elif move == 15:  # z2 up
            self.z_verticalMove(1, True)
        elif move == 16:  # z2 down
            self.z_verticalMove(1, False)
        elif move == 17:  # z3 up and side 4 counterclockwise
            self.z_verticalMove(2, True)
            self.rotateSaide(4, False)
        elif move == 18:  # z3 down and side 4 clockwise
            self.z_verticalMove(2, False)
            self.rotateSaide(4, True)

    def verticalMove(self, columnInd, forwardTurn):
        turns = 1 if forwardTurn else 3
        for i in range(turns):
            self.matrix[1][columnInd::3], self.matrix[2][columnInd::3], self.matrix[3][columnInd::3], self.matrix[4][columnInd::3] = \
                self.matrix[2][columnInd::3], self.matrix[3][columnInd::3], self.matrix[4][columnInd::3], self.matrix[1][columnInd::3]

    def z_verticalMove(self, rowInd, forwardTurn):
        turns = 1 if forwardTurn else 3
        if rowInd == 0:
            for i in range(turns):
                self.matrix[1][6:9], self.matrix[5][0::3], self.matrix[3][0:3], self.matrix[0][2::3] = \
                self.matrix[0][8::-3], self.matrix[1][6:9], self.matrix[5][6::-3], self.matrix[3][0:3]
        if rowInd == 1:
            for i in range(turns):
                self.matrix[1][3:6], self.matrix[5][1::3], self.matrix[3][3:6], self.matrix[0][1::3] = \
                self.matrix[0][7::-3], self.matrix[1][3:6], self.matrix[5][7::-3], self.matrix[3][3:6]
        if rowInd == 2:
            for i in range(turns):
                self.matrix[1][0:3], self.matrix[5][2::3], self.matrix[3][6:9], self.matrix[0][0::3] = \
                self.matrix[0][6::-3], self.matrix[1][0:3], self.matrix[5][8::-3], self.matrix[3][6:9]

    def rotateSaide(self, sideInd, clockwise):
        shift = 7 if clockwise else 3
        tmp = self.matrix[sideInd].copy()

        for i in range(len(tmp)):
            tmpInd = ((i+1)*shift) % 10 - 1
            tmp[i] = self.matrix[sideInd][tmpInd]
        self.matrix[sideInd] = tmp

    def horisontalMove(self, rowInd, rightTurn):
        turns = 1 if rightTurn else 3
        for i in range(turns):
            self.matrix[0][rowInd:rowInd+3], self.matrix[2][rowInd:rowInd+3], self.matrix[5][rowInd:rowInd+3], self.matrix[4][rowInd:rowInd+3] = \
                self.matrix[4][rowInd:rowInd+3], self.matrix[0][rowInd:rowInd+3], self.matrix[2][rowInd:rowInd+3], self.matrix[5][rowInd:rowInd+3]

    def getCubeArea(self):
        pass


def main():
    root = Tk()
    board = Board()
    root.geometry("400x750+600+100")
    root.mainloop()


if __name__ == "__main__":
    main()
