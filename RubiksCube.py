import random
from tkinter import Tk, Canvas, Frame, BOTH


class RubiksCube(Frame):
    def __init__(self):
        super().__init__()

        self.margin = 20
        self.edgeLen = 20
        self.matrix = []  # двумерный [лево, верх, фронт, низ, спина, право]
        self.colors = ['blue', 'yellow', 'red', 'white', 'orange', 'green']
        self.createCube()

        self.offset = ((0, 3 * self.edgeLen),
                       (3 * self.edgeLen, 0),
                       (3 * self.edgeLen, 3 * self.edgeLen),
                       (3 * self.edgeLen, 6 * self.edgeLen),
                       (3 * self.edgeLen, 9 * self.edgeLen),
                       (6 * self.edgeLen, 3 * self.edgeLen))

    def printCube(self):
        self.master.title("Cube")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        for facetInd in range(len(self.matrix)):
            for squareInd in range(9):
                offset = self.offset[facetInd]
                shift = squareInd // 3
                bbox = (self.margin+offset[0]+self.edgeLen*squareInd - self.edgeLen*3*shift,
                        self.margin+offset[1]+self.edgeLen*shift,
                        self.margin+offset[0]+self.edgeLen*squareInd+self.edgeLen - self.edgeLen*3*shift,
                        self.margin+offset[1]+self.edgeLen*shift+self.edgeLen)
                # верхнего левого и правого нижнего угла
                # x0, y0, x1, y1
                canvas.create_rectangle(*bbox, fill=self.colors[self.matrix[facetInd][squareInd]], activefill="black")

        canvas.pack(fill=BOTH, expand=1)

    def createCube(self):
        self.matrix = [[y+x*9 for y in range(0,9)] for x in range(6)]
        self.colors = [self.colors[x//9] for x in range(54)]

    def rotate(self, move):
        pass


def main():
    root = Tk()
    cube = RubiksCube()
    root.geometry("400x350+600+300")
    cube.printCube()
    root.mainloop()


if __name__ == "__main__":
    main()
