class Buff():
    def __init__(self,time = 0, value = 0, name = ""):
        self.name = name
        self.time = time
        self.value = value
        

def YellowPotion():
    return Buff(200,10,"Angle")
def GreenPotion():
    return Buff(200,3,"Speed")