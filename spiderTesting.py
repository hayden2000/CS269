import random
import math
import pygame
import numpy
from player import *
# create a game clock   


class Enemy:
    def __init__(self, win, x, y, image, width=90, height=50):
        self.x = x
        self.y = y
        self.center_x = x + (width/2)
        self.center_y = y + (height/2)
        self.win = win
        self.width = width
        self.height = height
        self.maxVel = 2
        self.downForce = 5
        self.currentSpeed = 1
        self.angle = 30
        self.image = image
        self.originalImg = image
        self.rotSurf = pygame.Surface((800, 600))
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
        
    def draw(self, screen, spider_img):
        screen.blit( self.rotImage, (self.x, self.y, self.width, self.height), self.rotImage.get_rect() )
        #pygame.draw.rect(self.win, (255, 0, 0), (int(self.x), int(self.y), int(self.width), int(self.height)))
        
    def move(self, player, frame):
        pygame.mixer.init()
        spyd=pygame.mixer.Sound('Audio/SpiderNew.aif')
        norm_player= ((player.getX()-0)/(800-0))
        norm_spyd= ((self.getX()-0)/(800-0))
        norm=abs((.25-abs(norm_player-norm_spyd)))
        spyd.set_volume(norm)
        
        pygame.mixer.Sound.play(spyd)

        radius = 120
        if(player.getX() == self.x):
            radius = abs(player.getY()-self.y)
        else:
            radius = math.sqrt((float(player.getX()) - float(self.getX()))**2 +(float( player.getY() )- float( self.getY() ))**2)
        if radius >= 150:
            self.random_move(frame)
        else:
            self.run_away(player.getX()+(player.width/2), (player.getY()+player.height/2))
    def move_x(self, speed):
        self.x += speed
        #print("speed = " + str(speed))
    def move_y(self, speed):
        self.y -= speed
    def random_move(self, frame):
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

    def run_away(self, player_x, player_y):
        diff_x = player_x -self.center_x
        diff_y = player_y -self.center_y
        playerAngle = numpy.degrees(numpy.arctan(diff_y/diff_x))
        self.angle = playerAngle+180
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)
        self.rotate()
        
    def rotate(self):
        width = (600*(numpy.cos(numpy.radians(90-self.angle)))) + (800*(numpy.cos(numpy.radians(self.angle))))
        height = (600*(numpy.sin(numpy.radians(90-self.angle)))) + (800*(numpy.sin(numpy.radians(self.angle))))         
        self.rotImage = pygame.Surface((600, 800))
        self.rotImage = pygame.transform.rotate(self.originalImg, self.angle)
        self.rect = self.rotImage.get_rect()