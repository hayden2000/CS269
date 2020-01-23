#Door.py

class Door:
    def __init__(self, x, y, image, exit):
        self.image = image
        self.x = x
        self.y = y
        self.exit = exit
        self.entrance = !exit
        self.unlocked = false
    
    #triggers next level load
    def win(player_x, player_y):
        if(self.exit and player_x == self.x and player_y == self.y and self.unlocked):
            #trigger next level
            nextLevel = 1
    
    #unlocks the door
    def unlock(self, unlock):
        self.unlocked = unlock
        #open door animation
        #light lamp
        
    
    def levelEnter(self):
        if(self.exit == false):
            animate=1
            #trigger open and close door animation
        else:
            print("Error: Incorrect Door Class")
    
            
        
    
    
