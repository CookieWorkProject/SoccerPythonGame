class Controller:
    def __init__(self, left = False, right = False, up = False, down = False, pause = False, confirm = False, cancel = False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.pause = pause
        self.confirm = confirm
        self.cancel = cancel
        
    #returns movement as a tuple
    def getMovementVectors(self):
        x = 0
        y = 0
        if self.left:
            x -= 1
        if self.right:
            x+=1
        if self.up:
            y -= 1
        if self.down:
            y+=1
        return (x,y)