from piece import piece
from player import player

class Game():
    
    def __init__(self, name1, name2, pos, startGame=False):
        self.players = [player(name1), player(name2)]
        self.pos = pos

        if(startGame):
            self.setPlayers()
            

 
    def setPlayers(self):  
        for i in range(0, 8):
            self.p1.pieces[i].setPos((0, i))
            self.p1.pieces[i+8].setPos((1, i))
            self.p2.pieces[i].setPos((7, i))
            self.p2.pieces[i+8].setPos((6, i))


    def atPos(self, pos):
        if(self.game[pos[0]][pos[1]] != None):
            return str(self.game[pos[0]][pos[1]])

    def move(player, piece, pos):
         pass 


    def startGame(self):
        turn = True
        for i in range(0, 1):
            print("\033[H\033[J")
            self.printBoard()
            if turn:
                input("\n" + self.p1.name + " select a piece: ")
                input(self.p1.name + " make a move: ")
                turn = False
            else:
                input("\n" + self.p2.name + " select a piece: ")
                input(self.p2.name + " make a move: ")
                turn = True 


