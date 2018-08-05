from piece import piece
from player import player

class board():
    
    def __init__(self, name1, name2):
        self.p1 = player(name1)
        self.p2 = player(name2) 
 
        self.game = [None] * 8
        for i in range(0, 8):
            self.game[i] = [None] * 8
 
    def setGame(self):  
        for i in range(0, 8):
            self.p1.pieces[i].setPos((0, i))
            self.p1.pieces[i+8].setPos((1, i))
            self.p2.pieces[i].setPos((7, i))
            self.p2.pieces[i+8].setPos((6, i))

        for pieces in self.p1.pieces:
            pos = pieces.getPosition()  
            self.game[pos[0]][pos[1]] = pieces

        for pieces in self.p2.pieces:
            pos = pieces.getPosition()  
            self.game[pos[0]][pos[1]] = pieces

    def atPos(self, pos):
        if(self.game[pos[0]][pos[1]] != None):
            return str(self.game[pos[0]][pos[1]])
 
    def printBoard(self):
        for i in range(7, -1, -1):
            print(str(self.game[i]))

    def startGame(self):
        


