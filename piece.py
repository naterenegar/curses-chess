class piece():
    def __init__(self, name, ty):
        self.alive = True
        self.name = name 
        self.ty = ty
        self.pos = (0,0)
        self.moved = False
            
    def __str__(self):
        return str(self.name)

    def setMoved(self):
        self.moved = True    

    def hasMoved(self):
        return self.moved
 
    def getPosition(self):
        return self.pos

    def getMoveSet(self):
        pass

    def getType(self):
        return ty
       
    def setPos(self, pos):
        if(self.isAlive()):
            self.pos = pos

    def kill(self):
        self.alive = False
        self.pos = (-1, -1)
 
    def isAlive(self):
        return self.alive
        
    def move(self):
        pass  


    __repr__ = __str__

