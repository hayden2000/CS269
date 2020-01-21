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
    background = pygame.image.load(os.path.join('images','setting.png')).convert()
    edges = screen.get_rect()
    p_height = 30
    p_width = 100
    platforms = []
    
    #first row
    platforms.append(Block(4,60, p_width, p_height, "block1.png"))
    platforms.append(Block(118,60, p_width, p_height, "block2.png"))
    platforms.append(Block(480, 60, p_width, p_height, "block1.png"))
    
    #second row
    platforms.append(Block(140,140, p_width, p_height, "block1.png"))
    platforms.append(Block(417,140, p_width, p_height, "block2.png"))
    platforms.append(Block(534,140, p_width/2, p_height, "block3.png"))
    
    #third row
    platforms.append(Block(5, 215, p_width, p_height, "block2.png"))
    platforms.append(Block(136, 215, p_width, p_height, "block1.png"))
    platforms.append(Block(266, 215, p_width, p_height, "block2.png"))
    platforms.append(Block(386, 215, p_width/2, p_height, "block3.png"))
    
    #fourth row
    platforms.append(Block(2, 302, p_width, p_height, "block1.png"))
    platforms.append(Block(210, 302, p_width, p_height, "block2.png"))
    platforms.append(Block(330, 302, p_width/2, p_height, "block3.png"))
    platforms.append(Block(480, 302, p_width, p_height, "block2.png"))
    
    #fifth row
    platforms.append(Block(2, 371, p_width, p_height, "block2.png"))
    platforms.append(Block(129, 371, p_width/2, p_height, "block3.png"))
    platforms.append(Block(267, 371, p_width/2, p_height, "block3.png"))
    platforms.append(Block(342, 371, p_width, p_height, "block1.png"))
    platforms.append(Block(578, 371, p_width, p_height, "block2.png"))
    
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
 
'''   
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

        
'''

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, platforms, width = 30, height = 50, mass = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = width
        self.height = height
        self.platforms = platforms
        self.mass = mass
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.position = vec(x, y)
        self.isJump = False
        self.hasKey = False
        
    def jumpCheck(self):
        if not(self.isJump):
            self.isJump =True

    def jump(self):
        #jump only if velocity y = 0
        if self.isJump:
            if self.vel.y == 0:
                self.vel.y = - 10
            else:
                self.isJump = False
    
    def update(self):
        self.acc = vec(0,0.98)
#       self.vel.x = 0
        keys = pygame.key.get_pressed()
        if self.position.y > 595:
            self.position.y = 0
        if self.position.x < 3:
            self.position.x = 3
        if self.position.x > 795:
            self.position.x = 795
        for platform in self.platforms:
            if self.rect.colliderect(platform):
                if self.isJump == False:
                    self.rect.bottom = platform.rect.top
                    self.vel.y = 0
                    self.acc.y = 0
                else:
                    #figure this out
                    print("jumping")
        if keys[pygame.K_LEFT]:
            if self.position.x < 0+self.width+self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = -1
        if keys[pygame.K_RIGHT]:
            if self.position.x > 800-self.width/2-self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = 1

        self.acc.x += self.vel.x*(-0.1)
        self.vel += self.acc
        self.position += self.vel + 0.5*self.acc
        self.rect.center = self.position



    