import random
import math
import pygame
import numpy
from player import *
# create a game clock
gameClock = pygame.time.Clock()

# class Player:
#     def __init__(self, win, x, y, width=30, height=50):
#         self.x = x
#         self.y = y
#         self.win = win
#         self.width = width
#         self.height = height
#         self.vel = 1
#         self.isJump = False
#         self.jumpCount = 9
#         self.left = False
#         self.right = False
#         self.walkCount = 0
# #list of image for walking right
# #list of image for walking left
#         self.gravity = 10
# 
#     def getIsJump(self):
#         return self.isJump
#     def setIsJump(self, jump):
#         self.isJump = jump
#     def getX(self):
#         return self.x
#     def getY(self):
#         return self.y
#     def getWidth(self):
#         return self.width
#     def getHeight(self):
#         return self.height
#     def getVel(self):
#         return self.vel
# 
#     def draw(self):
#         pygame.draw.rect(self.win,(255,0,0), (self.x, self.y, self.width, self.height))
# 
#     def moveLeft(self):
#         self.x-= self.vel
#         self.left = True
#         self.right = False
#     def moveRight(self):
#         self.x+=self.vel
#         self.left = False
#         self.right = True
#     def jump(self):
#         if not(self.isJump):
#             self.isJump = True
#             self.left = False
#             self.right = False
#         else:
#             if self.jumpCount>= -9:
#                 neg = 1
#                 if self.jumpCount < 0:
#                     neg = -1
#                 self.y -= (self.jumpCount**2)*0.5*neg
#                 self.jumpCount -=1
#             else:
#                 self.isJump = False
#                 self.jumpCount = 9
#     def random_move(self):
#         self.moveRight() 
#     def stand(self):
#         self.left = False
#         self.right = False    

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
        screen.blit( self.rotImage, (self.x, self.y, self.width, self.height),self.rotImage.get_rect() )
        #pygame.draw.rect(self.win, (255, 0, 0), (int(self.x), int(self.y), int(self.width), int(self.height)))
        
    def move(self, player, frame):
        radius= 120
        radius = math.sqrt(( float(player.getX() )-float( self.getX() ))**2 +(float( player.getY() )- float( self.getY() ))**2)
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
        # self.rotSurf = pygame.Surface((800, 600))
        # self.rotSurf = pygame.transform.rotate(self.rotSurf, self.angle)
        # self.rotSurf.blit(self.image, self.image.get_rect())
        #self.image = self.rotSurf
        
        
# def main():
#     # pygame.init()
# #     screenWidth = 800
# #     screenHeight = 600
#     # win = pygame.display.set_mode((screenWidth, screenHeight))
#     spider_img = pygame.image.load("Assets/Spider.png").convert_alpha()
#     #pygame.display.set_caption("Test")
#     #player = Player(win, 300, 200)
#     spider = Enemy(screen, 300, 500, spider_img)
#     frame = 0
#     #run = True
#     while run:
#         frame += 1
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#         win.fill( (0,0,0) )
#         spider.move(player, frame)
#         spider.draw(screen, spider_img)
#         # player.draw()
# #         pygame.display.update()
# #         gameClock.tick(30)
#     pygame.quit()
# if __name__ == "__main__":
#     main()
    