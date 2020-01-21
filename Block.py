#Natalie Lunbeck
#CS269: Game Design
#Shadow Puppets

#This class creates a block object for platforms
import pygame
import os
import sys

class Block(pygame.sprite.Sprite):
    #block code that tells the program what type of block this will be
    #0 = platform, 1 = wall
    block_type = 0
    
    def __init__(self, x_pos, y_pos, width, height, sprite):
        #creating a new block
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',sprite)).convert()
        #loading a sprite in and giving it a transparent background
        self.image.convert_alpha()
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        #self.image.set_colorkey()
        #giving a rigidbody
        self.rect = self.image.get_rect()
        #setting coordinates
        self.rect.x = x_pos
        self.rect.y = y_pos
        #block defaults to platform
        
    def getX():
        return self.rect.x
    
    def getY(): 
        return self.rect.y
    
    def setX(new_x):
        self.rect.x = new_x
        
    def setY(new_y):
        self.rect.y = new_y
        
    def setBlock(num):
        #change block to either a platform or wall
        if num != 0:
            self.block_type = 1
        else:
            self.block_type = 0
            
            
def layout_level1(screen):
    #screen = pygame.display.set_mode([800,600])
    background = pygame.image.load(os.path.join('images','background.png')).convert()
    edges = screen.get_rect()
    p_height = 30
    p_width = 100
    platforms = pygame.sprite.Group()
    
    #first row
    platforms.add(Block(4,60, p_width, p_height, "block1.png"))
    platforms.add(Block(118,60, p_width, p_height, "block2.png"))
    platforms.add(Block(480, 60, p_width, p_height, "block1.png"))
    
    #second row
    platforms.add(Block(140,140, p_width, p_height, "block1.png"))
    platforms.add(Block(417,140, p_width, p_height, "block2.png"))
    platforms.add(Block(534,140, p_width/2, p_height, "block3.png"))
    
    #third row
    platforms.add(Block(5, 215, p_width, p_height, "block2.png"))
    platforms.add(Block(136, 215, p_width, p_height, "block1.png"))
    platforms.add(Block(266, 215, p_width, p_height, "block2.png"))
    platforms.add(Block(386, 215, p_width/2, p_height, "block3.png"))
    
    #fourth row
    platforms.add(Block(2, 302, p_width, p_height, "block1.png"))
    platforms.add(Block(210, 302, p_width, p_height, "block2.png"))
    platforms.add(Block(330, 302, p_width/2, p_height, "block3.png"))
    platforms.add(Block(480, 302, p_width, p_height, "block2.png"))
    
    #fifth row
    platforms.add(Block(2, 371, p_width, p_height, "block2.png"))
    platforms.add(Block(129, 371, p_width/2, p_height, "block3.png"))
    platforms.add(Block(267, 371, p_width/2, p_height, "block3.png"))
    platforms.add(Block(342, 371, p_width, p_height, "block1.png"))
    platforms.add(Block(578, 371, p_width, p_height, "block2.png"))
    
    return platforms
    

class Layout():
    #dimensions are 800x600
    level = 1
    def __init__(self, cur_level, screen):
        self.level = cur_level
        if cur_level == 1:
            layout_level1(screen)
        else:
            print("level does not exist yet")

if __name__=="__main__":
    print(layout_level1())
    
class Pickup():
    pickup_type = 1
    #this tells us what type of object we are creating
    #1 = key
    def __init__(self, obj_type = 1, x_pos, y_pos):
        self.pickup_type = obj_type
        self.image = pygame.Surface((20, 20))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        #setting coordinates
        self.rect.x = x_pos
        self.rect.y = y_pos
        if obj_type == 1:
            print("this is a key")
            #set sprite to key
        else:
            print("object does not exist yet")

        
    
    