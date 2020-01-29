import random
import math
import pygame
import numpy
from player import *
from lighting import *
# create a game clock   

class Enemy:
    def __init__(self, win, x, y, image, lampList, width=75, height=55):
        self.x = x
        self.y = y
        self.center_x = x + (width/2)
        self.center_y = y + (height/2)
        self.win = win
        self.width = width
        self.height = height
        self.maxVel = 10
        self.downForce = 5
        self.currentSpeed = 1
        self.angle = 30
        self.originalImg = image
        self.rotImage = pygame.Surface((400, 300))
        #temp
        self.rect = image.get_rect()
        self.dead = False
        self.whichImg = 0
        self.lampList = lampList
        self.prevFunct = 0
        self.currentFrame = 0
#list of image for walking right
#list of image for walking left
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def get_rect(self):
    	return pygame.Rect(self.x, self.y, width, height)
    	
    def isDead(self):
    	return self.dead
    
    def get_rect(self):
    	return pygame.Rect(self.x, self.y, self.width, self.height)
    	
    def get_rotRect(self):
        rect = self.rect
        rect.center = (self.center_x, self.center_y)
        return rect
    
    def get_images(self, x, y):
        sprite = pygame.image.load('Assets/Spider_Sprite.png').convert_alpha()
        getimage = pygame.Surface((75,55))
        getimage.set_colorkey((0,0,0))
        getimage.blit(sprite,(0,0),(x,y,75,55))
        getimage = pygame.transform.scale(getimage,(75, 55))
        return getimage.convert_alpha()
        
    # def load_images(self):
#     	
#     
#     
#         for pic in self.standing:
#             pic.set_colorkey((0,0,0))
#         self.walkRight = [self.get_images(20,140,29,50), self.get_images(59, 20, 29, 50),self.get_images(59, 80, 29, 50),
#                           self.get_images(59,140,29,50), self.get_images(98, 20, 29, 50),self.get_images(137, 20, 29, 50),
#                           self.get_images(176,20,29,50), self.get_images(98, 80, 29, 50),self.get_images(98, 140, 29, 50),
#                           self.get_images(137, 80, 29, 50)]
#         self.walkLeft = []
#         for pic in self.walkRight:
#             pic.set_colorkey((0,0,0))
#             self.walkLeft.append(pygame.transform.flip(pic, True, False))
#         self.jumpSprite = []
    
    
    def get_rotImage(self):
        return self.rotImage
    
    def draw(self, screen):
        if not self.dead:
        	screen.blit( self.rotImage, (self.x, self.y, self.width, self.height), self.rotImage.get_rect() )
        #pygame.draw.rect(self.win, (255, 0, 0), (int(self.x), int(self.y), int(self.width), int(self.height)))
        
    def move(self, player, frame):
        pygame.mixer.init()
        spyd=pygame.mixer.Sound('Audio/SpiderNew.ogg')
        norm_player= ((player.getX()-0)/(800-0))
        norm_spyd= ((self.getX()-0)/(800-0))
        norm=abs((.25-abs(norm_player-norm_spyd)))
        spyd.set_volume(norm)
        
        pygame.mixer.Sound.play(spyd)
        
       
        num = frame % 5
        if num == 1:
            #print("x: " +str(int(self.x)))
            #print("y:" + str(int(self.y)))
            if(self.whichImg >= 5):
                 self.whichImg = 0
            self.originalImg = self.get_images(20, 20 + (self.whichImg * 75))
            self.whichImg += 1
        	
        radius = 120
        if(player.getX() == self.x):
        	radius = abs(player.getY()-self.y)
        else:
        	radius = math.sqrt((float(player.getX()) - float(self.getX()))**2 +(float( player.getY() )- float( self.getY() ))**2)
        
        if radius <= 120:
            self.run_away(player.getX()+(player.width/2), (player.getY()+player.height/2))
        else:
            lampLit =False
            for lamp in self.lampList:
                lampLit = lamp.isLit
                if(lampLit == True):
                    break
            if(lampLit == True):
                if(self.prevFunct == 1):
                    self.random_move(frame)
                    self.currentFrame = frame
                elif(self.currentFrame != 0 and frame < self.currentFrame+40 ):
                    self.random_move(frame)
                else:
                    self.currentFrame = 0
                    self.find_lamp()
            else:
                self.random_move(frame)
            
            
    def move_x(self, speed):
        self.x += speed
        self.center_x = self.x + (self.width/2)
        
        #print("speed = " + str(speed))
        
    def move_y(self, speed):
        self.y -= speed
        self.center_y = self.y + (self.height/2)
        
    def random_move(self, frame):
        self.prevFunct = 0
        #print("random move")
        if(self.angle >= 360 or self.angle <= -360):
            self.angle = self.angle%360
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)
        if(frame%10 == 1):
            chance = random.random()
            if(chance < .25):
                self.angle += 5
            elif(chance < .5):
                self.angle -= 5
            else:
                self.angle += 0
        if(self.x + self.width >= self.win.get_width() or self.x < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        if(self.y + self.height >= self.win.get_height() or self.y < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        self.rotate()
        #print(self.angle)    

    def find_lamp(self):
        #print("finding lamp")
        self.prevFunct = 2
        closeLamp = self.lampList[0]
        closeDist = 10000
        for lamp in self.lampList:
            if(lamp.isLit == True):
                dist = numpy.sqrt(((self.center_x - lamp.coors[0])**2 + (self.center_y - lamp.coors[1])**2 ))
                if(dist < closeDist):
                    closeDist = dist
                    closeLamp = lamp
        temp_angle = numpy.degrees(numpy.arctan((self.center_y - closeLamp.coors[1]) / (closeLamp.coors[0] - self.center_x)))
        if(self.center_x > closeLamp.coors[0] and self.center_y > closeLamp.coors[1]):
            self.angle = 180 - (temp_angle)
        elif(self.center_x > lamp.coors[0] and self.center_y < lamp.coors[1]):
            self.angle = -(180 - (temp_angle))
        else:
            self.angle = temp_angle
        
        if(self.x + self.width >= self.win.get_width() or self.x < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
            self.x = 300
        if(self.y + self.height >= self.win.get_height() or self.y < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
            self.y = 400
        
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        
        
            
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)         
        self.rotate()
    	
    	
    def run_away(self, player_x, player_y):
        self.prevFunct = 1
        #print("run away")
        diff_x = player_x -self.center_x
        diff_y = player_y -self.center_y
        if diff_x == 0:
        	diff_x = 1
        playerAngle = numpy.degrees(numpy.arctan(diff_y/diff_x))
        self.angle = playerAngle+180
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)
        
        if(self.x + self.width >= self.win.get_width() or self.x < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        if(self.y + self.height >= self.win.get_height() or self.y < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        
        self.rotate()
        
    def rotate(self):
        width = (600*(numpy.cos(numpy.radians(90-self.angle)))) + (800*(numpy.cos(numpy.radians(self.angle))))
        height = (600*(numpy.sin(numpy.radians(90-self.angle)))) + (800*(numpy.sin(numpy.radians(self.angle))))         
        self.rotImage = pygame.Surface((600, 800))
        self.rotImage = pygame.transform.rotate(self.originalImg, self.angle)
        self.rect = self.rotImage.get_rect()
        
    def collideSpider(self):
    	#print("collided")
    	self.maxVel= 0
    	self.image = pygame.Surface((800, 600), pygame.SRCALPHA)
    	self.originalImage = pygame.Surface((800, 600), pygame.SRCALPHA)
    	self.rotImage = pygame.Surface((100, 100), pygame.SRCALPHA)
    	self.dead = True
    	