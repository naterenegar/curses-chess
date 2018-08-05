from piece import piece
from ptypes import ptypes


class player():

    def resetPieces(self):
        tmp = [None] * 16 
        tmp[0] = piece(self.name + '.r1', ptypes.ROOK)
        tmp[1] = piece(self.name + '.k1', ptypes.KNIGHT)
        tmp[2] = piece(self.name + '.b1', ptypes.BISHOP)
        tmp[3] = piece(self.name + '.K', ptypes.KING)
        tmp[4] = piece(self.name + '.Q', ptypes.QUEEN)
        tmp[5] = piece(self.name + '.b2', ptypes.BISHOP)
        tmp[6] = piece(self.name + '.k2', ptypes.KNIGHT)
        tmp[7] = piece(self.name + '.r2', ptypes.ROOK)
        for i in range(8, 16):
            tmp[i] = piece(self.name + '.p' + str(i - 7), ptypes.PAWN) 
        
        return tmp

    def __init__(self, name):
        self.name = name
        self.pieces = self.resetPieces()     

       
     
