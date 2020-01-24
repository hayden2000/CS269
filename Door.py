#Door.py

import pygame

door_img = pygame.image.load("Assets/door.png")

class Door:
    def __init__(self, midbottom, exit):
        self.image = door_img
        
        self.center = ( midbottom[0], midbottom[1] - (self.image.get_height()/2) )
        self.rect = door_img.get_rect()
        self.rect.center = self.center
        
        self.exit = exit
        self.entrance = not exit
        self.unlocked = False
    
    #triggers next level load
    def win(self, player):
        if(self.exit and player.rect.collidepoint( self.center ) and self.unlocked):
            #trigger next level
            return True
    
    #unlocks the door
    def unlock(self):
        self.unlocked = True
        #open door animation/sound
        #light lamp
        
    
    def levelEnter(self):
        if(self.exit == False):
            animate=1
            #trigger open and close door animation
        else:
            print("Error: Incorrect Door Class")
    
            
        
    
    
