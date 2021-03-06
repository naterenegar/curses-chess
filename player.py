from piece import piece
from ptypes import ptypes


class player():

    def setPieces(self):
        tmp = [None] * 16 
        tmp[0] = piece('R1', ptypes.ROOK)
        tmp[1] = piece('k1', ptypes.KNIGHT)
        tmp[2] = piece('B1', ptypes.BISHOP)
        tmp[3] = piece('Kg', ptypes.KING)
        tmp[4] = piece('Qn', ptypes.QUEEN)
        tmp[5] = piece('B2', ptypes.BISHOP)
        tmp[6] = piece('k2', ptypes.KNIGHT)
        tmp[7] = piece('R2', ptypes.ROOK)
        for i in range(8, 16):
            tmp[i] = piece('P' + str(i - 7), ptypes.PAWN) 
        
        return tmp

    def __init__(self, name):
        self.name = name
        self.pieces = self.setPieces()     

       
     
