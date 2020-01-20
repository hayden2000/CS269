import random
import math
import pygame
import numpy
# create a game clock
gameClock = pygame.time.Clock()

class Player:
    def __init__(self, win, x, y, width=30, height=50):
        self.x = x
        self.y = y
        self.win = win
        self.width = width
        self.height = height
        self.vel = 1
        self.isJump = False
        self.jumpCount = 9
        self.left = False
        self.right = False
        self.walkCount = 0
#list of image for walking right
#list of image for walking left
        self.gravity = 10

    def getIsJump(self):
        return self.isJump
    def setIsJump(self, jump):
        self.isJump = jump
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getVel(self):
        return self.vel

    def draw(self):
        pygame.draw.rect(self.win,(255,0,0), (self.x, self.y, self.width, self.height))

    def moveLeft(self):
        self.x-=self.vel
        self.left = True
        self.right = False
    def moveRight(self):
        self.x+=self.vel
        self.left = False
        self.right = True
    def jump(self):
        if not(self.isJump):
            self.isJump = True
            self.left = False
            self.right = False
        else:
            if self.jumpCount>= -9:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount**2)*0.5*neg
                self.jumpCount -=1
            else:
                self.isJump = False
                self.jumpCount = 9
    def random_move(self):
        self.moveRight()
  
    def stand(self):
        self.left = False
        self.right = False
    

class Enemy:
    def __init__(self, win, x, y, image, width=90, height=50):
        self.x = x
        self.y = y
        self.win = win
        self.width = width
        self.height = height
        self.maxVel = 2
        self.downForce = 5
        self.currentSpeed = 1
        self.angle = 30
        self.image = image
        self.rotSurf = pygame.Surface( (800,600) )
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

    def draw(self):
        pygame.draw.rect(self.win,(255,0,0), (int(self.x), int(self.y), int(self.width), int(self.height)))

    def move_x(self,speed):
        self.x += speed
        #print("speed = " + str(speed))
        
    def move_y(self,speed):
        self.y -= speed
    def random_move(self,frame):
        if(self.angle >= 360 or self.angle <=-360):
            self.angle = self.angle%360
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)
        if(frame%25 == 1):
            chance = random.random()
            if(chance < .25):
                self.angle +=25
            elif(chance <.5):
                self.angle -= 25
            else:
                self.angle +=0
            self.rotate()
        if(self.x + self.width >= self.win.get_width() or self.x < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        if(self.y + self.height >= self.win.get_height() or self.y < 0):
            self.angle = -(90 -self.angle)
            self.rotate()
        self.rotate()
        #print(self.angle)    

    def run_away(self, player_x, player_y):
        diff_x = player_x -self.x
        diff_y = player_y -self.y
        playerAngle = numpy.degrees(numpy.arctan(diff_y/diff_x))
        self.angle = playerAngle+180
        ratio_x = numpy.cos(numpy.radians(self.angle))
        ratio_y = numpy.sin(numpy.radians(self.angle))
        #if collide move other way
        self.move_x(self.maxVel*ratio_x)
        self.move_y(self.maxVel*ratio_y)
        #self.rotate()
        
    def rotate(self):
        self.rotSurf.blit(self.image, self.image.get_rect())
        self.rotSurf = pygame.transform.rotate(self.rotSurf, self.angle)
       
            
def main():
    pygame.init()
    screenWidth = 800
    screenHeight = 600
    win = pygame.display.set_mode((screenWidth,screenHeight)) 
    spider_img = pygame.image.load( "Spider.png" ).convert_alpha()
    pygame.display.set_caption("Test")
    player = Player(win, 300, 200)
    spider = Enemy(win, 300, 500, spider_img)
    frame = 0
    run = True
    while run:
        frame+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        radius = math.sqrt((float(player.getX())-float(spider.getX()))**2 +(float(player.getY())- float(spider.getY()))**2)
        #print (radius)
        if radius >= 150:
            spider.random_move(frame)
        else:
            spider.run_away(player.getX()+ (player.getWidth()/2), (player.getY()+player.getHeight()/2))
        win.fill((0, 0, 0))
        player.draw()
        spider.draw()
        pygame.display.update()
        gameClock.tick(30)
    pygame.quit()
if __name__ == "__main__":
    main()