#Natalie Lunbeck
#CS269: Game Design
#Shadow Puppets

#This class creates a block object for platforms
import pygame
import os
import sys
from pygame.locals import *

bg = pygame.image.load('images/setting.png')
b1 = pygame.image.load('images/block1.png')
b2 = pygame.image.load('images/block2.png')
b3 = pygame.image.load('images/block3.png')

class Block(pygame.sprite.Sprite):
    #block code that tells the program what type of block this will be
    #0 = platform, 1 = wall
    block_type = 0
    
    def __init__(self, x_pos, y_pos, width, height, sprite):
        #creating a new block
        pygame.sprite.Sprite.__init__(self)
        if sprite == "block1.png":
            self.image = b1
        elif sprite == "block2.png":
            self.image = b2
        elif sprite == "block3.png":
            self.image = b3
        else:
            self.image = b1
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        #loading a sprite in and giving it a transparent background
        #self.image.convert_alpha()
        #self.image = pygame.Surface((width, height))
        #self.image.fill((0,0,255))
        #self.image.set_colorkey()
        #giving a rigidbody
        self.rect = self.image.get_rect()
        #setting coordinates
        self.rect.x = x_pos
        self.rect.y = y_pos
        new_height = height - 2
        #makes the rect 2 px high
        self.rect.inflate(0, -40)
        print(self.rect)
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
    p_height = 50
    p_width = 150
    platforms = []
    ar_x = 1.3
    ar_y = 1.5
    
    #first row
    platforms.append(Block(int(ar_x*4),int(ar_y*60), p_width, p_height, "block1.png"))
    platforms.append(Block(int(ar_x*118),int(ar_y*60), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*480), int(ar_y*60), p_width, p_height, "block1.png"))
    
    #second row
    platforms.append(Block(int(ar_x*140),int(ar_y*140), p_width, p_height, "block1.png"))
    platforms.append(Block(int(ar_x*417),int(ar_y*140), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*534),int(ar_y*140), p_width/2, p_height/2, "block3.png"))
    
    #third row
    platforms.append(Block(int(ar_x*5), int(ar_y*215), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*110), int(ar_y*215), p_width, p_height, "block1.png"))
    platforms.append(Block(int(ar_x*272), int(ar_y*215), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*386), int(ar_y*215), p_width/2, p_height/2, "block3.png"))
    
    #fourth row
    platforms.append(Block(int(ar_x*2), int(ar_y*302), p_width, p_height, "block1.png"))
    platforms.append(Block(int(ar_x*210), int(ar_y*302), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*330), int(ar_y*302), p_width/2, p_height/2, "block3.png"))
    platforms.append(Block(int(ar_x*480), int(ar_y*302), p_width, p_height, "block2.png"))
    
    #fifth row
    platforms.append(Block(int(ar_x*2), int(ar_y*371), p_width, p_height, "block2.png"))
    platforms.append(Block(int(ar_x*119), int(ar_y*371), p_width/2, p_height/2, "block3.png"))
    platforms.append(Block(int(ar_x*257), int(ar_y*371), p_width/2, p_height/2, "block3.png"))
    platforms.append(Block(int(ar_x*372), int(ar_y*371), p_width, p_height, "block1.png"))
    platforms.append(Block(int(ar_x*478), int(ar_y*371), p_width, p_height, "block2.png"))
    
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
        self.currentSprite = 0
        self.lastTicks = 0
        self.walking = False
        self.load_images()
        self.image = self.standing[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
#        self.rect.left = x-15
#        self.rect.right = x+15
#        self.rect.bottom = y-25
#        self.rect.top = y+25
        print(self.rect)
        print(self.rect.top)
        print(self.rect.bottom)
        self.width = width
        self.height = height
        self.platforms = platforms
        self.mass = mass
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.position = vec(x, y)
        self.platforming = True
        self.isJump = False
    def get_images(self, a, b, wid, hei):
        sprite = pygame.image.load('Walking.png').convert()
        getimage = pygame.Surface((wid,hei))
        getimage.blit(sprite,(0,0),(a,b,wid,hei))
        getimage = pygame.transform.scale(getimage,(wid, hei))
        return getimage

    def load_images(self):
        self.standing = [self.get_images(20, 20, 29, 50), self.get_images(20, 80, 29, 50)]
        for pic in self.standing:
            pic.set_colorkey((0,0,0))
        self.walkRight = [self.get_images(20,140,29,50), self.get_images(59, 20, 29, 50),self.get_images(59, 80, 29, 50),
                          self.get_images(59,140,29,50), self.get_images(98, 20, 29, 50),self.get_images(137, 20, 29, 50),
                          self.get_images(176,20,29,50), self.get_images(98, 80, 29, 50),self.get_images(98, 140, 29, 50),
                          self.get_images(137, 80, 29, 50)]
        self.walkLeft = []
        for pic in self.walkRight:
            pic.set_colorkey((0,0,0))
            self.walkLeft.append(pygame.transform.flip(pic, True, False))
        self.jumpSprite = []
        
    def jumpCheck(self):
        if not(self.isJump):
            self.isJump =True

    def jump(self):
        #jump only if velocity y = 0
        if self.isJump:
            if self.vel.y == 0:
                self.vel.y = -17
                self.isJump = False
        # self.rect.x += 1
#         hits=pygame.sprite.spritecollide(self, self.platforms, False)
#         self.rect.x -= 1
      #   if hits:
#             self.vel.y = -17

    def hitX(self):
        for platform in self.platforms:
            #hit = self.rect.colliderect(platform)
            
            if self.rect.colliderect(platform):
                #left
                if self.vel.x > 0:
                    self.position.x = platform.rect.left - (self.width/2)
                    self.vel.x = 0
                #right
                elif self.vel.x < 0:
                    self.position.x = platform.rect.right + (self.width/2)
                    self.vel.x = 0
                        
    def hitY(self):
        for platform in self.platforms:
            #hit = self.rect.colliderect(platform)
            
            if self.rect.colliderect(platform):
                #top
                if self.vel.y > 0:
                    self.position.y = platform.rect.top
                    self.vel.y = 0
                #bottom
                elif self.vel.y < 0:
                    self.position.y = platform.rect.bottom + self.height
                    self.vel.y = 0


    def update(self):
        self.motion()
        self.acc = vec(0,0.98)
        #self.hit()
        #self.acc = vec(0,0.98)
#       self.vel.x = 0
        keys = pygame.key.get_pressed()
        if self.position.y > 595:
            self.position.y = 0
        if self.position.x < 5:
            self.position.x = 5
        if self.position.x > 795:
            self.position.x = 795
        #print(self.rect.x)
        #print(self.rect.y)
        
        if keys[pygame.K_LEFT]:
            if self.position.x < 0+self.width+self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = -0.9
        if keys[pygame.K_RIGHT]:
            if self.position.x > 800-self.width/2-self.vel.x:
                self.acc.x = 0
                self.vel.x = 0
            else:
                self.acc.x = 0.9

        self.acc.x += self.vel.x*(-0.1)
        self.vel += self.acc
        if abs(self.vel.x) < 0.6:
            self.vel.x = 0 
        
        self.position[0] += self.vel[0] + 0.5*self.acc[0]
        self.rect.midbottom = self.position
        
        self.hitX()
        
        self.position[1] += self.vel[1] + 0.5*self.acc[1]
        self.rect.midbottom = self.position
        
        self.hitY()
        
        self.rect.midbottom = self.position

    def motion(self):
        nowTicks = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if nowTicks - self.lastTicks > 50:
                self.lastTicks = nowTicks
                if self.vel.x > 0:
                    self.currentSprite = (self.currentSprite+1)%len(self.walkRight)
                    self.image = self.walkRight[self.currentSprite] 
                if self.vel.x < 0:
                    self.currentSprite = (self.currentSprite+1)%len(self.walkLeft)
                    self.image = self.walkLeft[self.currentSprite]
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.walking and not self.isJump:
            if nowTicks - self.lastTicks > 500:
                self.lastTicks = nowTicks
                self.currentSprite = (self.currentSprite+1)% len(self.standing)
                bottom = self.rect.bottom
                self.image = self.standing[self.currentSprite]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


    