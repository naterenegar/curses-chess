from piece import piece
from player import player
import curses


class Game():
    
    def __init__(self, name1, name2, pos, scr, startGame=False):
        self.players = [player(name1), player(name2)]
        self.pos = pos
        self.scr = scr
        self.setPlayers()
 
    def setPlayers(self):  
        for i in range(0, 8):
            self.players[0].pieces[i].setPos((0, i))
            self.players[0].pieces[i+8].setPos((1, i))
            self.players[1].pieces[i].setPos((7, i))
            self.players[1].pieces[i+8].setPos((6, i))


    def atPos(self, pos):
        if(self.game[pos[0]][pos[1]] != None):
            return str(self.game[pos[0]][pos[1]])

    def move(self, player, piece, pos):
        p = self.players[player]
        p_pos = p.pieces[piece].getPosition()
        pstr = str(p.pieces[piece])

        # Draw over old position
        if((p_pos[0] % 2 == 0 and p_pos[1] % 2 == 0) or (p_pos[0] % 2 == 1 and p_pos[1] % 2 == 1)):
            self.scr.addstr(self.pos[p_pos[0]][p_pos[1]][0], self.pos[p_pos[0]][p_pos[1]][1], "  ", curses.color_pair(2))  
        else:
            self.scr.addstr(self.pos[p_pos[0]][p_pos[1]][0], self.pos[p_pos[0]][p_pos[1]][1], "  ", curses.color_pair(1))  
           

 
        p.pieces[piece].setPos(pos)
        self.scr.addstr(self.pos[pos[0]][pos[1]][0], self.pos[pos[0]][pos[1]][1], pstr, curses.color_pair(player+3))  
        self.scr.refresh()

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


