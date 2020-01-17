import pygame
import random
import math
# create a game clock
gameClock = pygame.time.Clock()

class Player:
    def __init__(self, win, x, y, width=30, height=50, mass=1):
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
    def __init__(self, win, x, y, width=90, height=40, mass=1):
        self.x = x
        self.y = y
        self.win = win
        self.width = width
        self.height = height
        self.vel = 3
        self.isJump = False
        self.jumpCount = 9
        self.left = False
        self.right = False
        self.walkCount = 0
        self.currentDirection = 0
        self.moveDirection = 0
        self.downForce = 5
        self.jumping = False
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
    # def moveSetup(self):
    #     if(self.jumping)

    def random_move(self,frame):
        #if collide move other way
        if(self.moveDirection == 0):
            self.moveRight()
        else:
            self.moveLeft()
        if(frame%50 == 1):
            chance = random.random()
            jumpChance = random.random()
            print(jumpChance)
            print(chance)
            if(chance > .8):
                if(self.currentDirection == 0):
                    self.moveDirection = 0
                else:
                    self.moveDirection = 1
                    self.currentDirection = 1
            elif(self.currentDirection == 0):
                self.moveDirection = 1
                self.currentDirection = 1
            else:
                self.moveDirection = 0
                self.currentDirection = 0
            if(jumpChance < .15):
                self.jumping = True

    def run_away(self, player_x, player_y):
        if(player_x < self.y):
            self.moveLeft()
        else:
            self.moveRight()
    def stand(self):
        self.left = False
        self.right = False
            
def main():
    pygame.init()
    screenWidth = 800
    screenHeight = 600
    win = pygame.display.set_mode((800,600)) 
    pygame.display.set_caption("Test")
    player = Player(win, 300, 200)
    spider = Enemy(win,300, 500)
    frame = 0
    run = True
    while run:
        frame+=1
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        r = math.sqrt((float(player.getX())-float(spider.getX()))**2 +(float(player.getY())- float(spider.getY()))**2)
        print (r)
        radius =120
        if radius >= 100:
            spider.random_move(frame)
        else:
            spider.run_away(player.getX(),player.getY())
        win.fill((0,0,0))
        player.draw()
        spider.draw()
        pygame.display.update()
        gameClock.tick(30)
    pygame.quit()
if __name__ == "__main__":
    main()