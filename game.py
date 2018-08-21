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

    def checkPos(self, pos):
        # Return piece number 0-15 if player 0 has a piece at pos,
        # 16-31 if player 1 has a piece at pos, and -1 if pos is empty 
        for i in range(0, 16):
            if(self.players[0].pieces[i].getPosition() == pos):
                return i
            elif(self.players[1].pieces[i].getPosition() == pos):
                return i + 16

        return -1


    def move(self, player, piece, pos):

        p = self.players[player]
        op = self.players[1 if player == 0 else 0]
        pc = p.pieces[piece]
        p_pos = pc.getPosition()
        pstr = str(p.pieces[piece])

        # Change direction of check based on which player
        pmod = 1 if player == 0 else -1

        # Flag for valid move
        valid = True 

        # Check what is at space we're moving to 
        check = self.checkPos(pos)
        if(check != -1): 
            if(player == 0 and check < 16):
                valid = False
            elif(player == 1 and check > 15):
                valid = False

        # Pawn logic 
        if(piece > 7 and piece < 16):
            bad_row = pos[0] - p_pos[0] != (1 * pmod)
            bad_row2 = pos[0] - p_pos[0] != (2 * pmod)
            bad_col = pos[1] - p_pos[1] != 0
            bad_kill = pos[1] - p_pos[1] != 1 and pos[1] - p_pos[1] != -1

            # If we're moving diagonal to kill it must be 1 space
            if(check != -1):
                if(bad_row or bad_kill):
                    valid = False
                else:
                    tmp_pc = check - 16 if check > 15 else check
                    op.pieces[tmp_pc].kill()
            else:
                if(pc.hasMoved()):
                    if(bad_row or bad_col):
                        valid = False 
                else:
                    if((bad_row and bad_row2) or bad_col):
                        valid = False
                    pc.setMoved()
        


        if(valid):
            # Draw over old position if so
            if((p_pos[0] % 2 == 0 and p_pos[1] % 2 == 0) or (p_pos[0] % 2 == 1 and p_pos[1] % 2 == 1)):
                self.scr.addstr(self.pos[p_pos[0]][p_pos[1]][0], self.pos[p_pos[0]][p_pos[1]][1], "  ", curses.color_pair(2))  
            else:
                self.scr.addstr(self.pos[p_pos[0]][p_pos[1]][0], self.pos[p_pos[0]][p_pos[1]][1], "  ", curses.color_pair(1))  
 
            p.pieces[piece].setPos(pos)
            self.scr.addstr(self.pos[pos[0]][pos[1]][0], self.pos[pos[0]][pos[1]][1], pstr, curses.color_pair(player+3))  
            self.scr.addstr(1, 1, "             ")
        else:
            self.scr.addstr(1, 1, "INVALID MOVE!")


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


