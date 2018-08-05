class piece():
    def __init__(self, name, ty):
        self.alive = True
        self.name = name 
        self.ty = ty
        self.pos = (0,0)
            
    def __str__(self):
        return str(self.name)
     
    def getPosition(self):
        return self.pos

    def getMoveSet(self):
        pass

    def getType(self):
        return ty
       
    def setPos(self, pos):
        self.pos = pos
 
    def isAlive(self):
        return self.alive
        
    def move(self):
        pass  


    __repr__ = __str__

