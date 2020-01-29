import pygame 
vec = pygame.math.Vector2
from Block import *
from Key import *
from spiderTesting import *

#vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, platforms, width = 30, height = 50, mass = 1):
        pygame.sprite.Sprite.__init__(self)
        self.currentSprite = 0
        self.lastTicks = 0
        self.walking = False
        self.load_images()
        self.image = self.standingRight[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.lightRect = lightAlpha.get_rect()
        self.lightRect.center = (x,y)
        #self.rect.left = x-15
        #self.rect.right = x+15
        #self.rect.bottom = y-25
        #self.rect.top = y+25
        #print(self.rect)
        #print(self.rect.top)
        #print(self.rect.bottom)
        self.width = width
        self.height = height
        self.platforms = platforms
        self.mass = mass
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.position = vec(x, y)
        self.platforming = True
        self.isJump = False
        self.hasKey = False
        self.k = Key(-100, -100, 50)
        self.isRight = True
        
    def get_images(self, a, b, wid, hei):
        sprite = pygame.image.load('Assets/Walking.png').convert()
        getimage = pygame.Surface((wid,hei))
        getimage.blit(sprite,(0,0),(a,b,wid,hei))
        getimage = pygame.transform.scale(getimage,(wid, hei))
        return getimage

    def load_images(self):
        #self.standing = [self.get_images(20, 20, 29, 50), self.get_images(20, 80, 29, 50)]
        
        self.standingRight = [self.get_images(20, 20, 29, 50), self.get_images(20, 80, 29, 50)]
        for pic in self.standingRight:
            pic.set_colorkey((0,0,0))
            
        self.standingLeft = []
        for pic in self.standingRight:
            self.standingLeft.append(pygame.transform.flip(pic, True, False))
        
        
        self.walkRight = [self.get_images(20,140,29,50), self.get_images(59, 20, 29, 50),self.get_images(59, 80, 29, 50),
                          self.get_images(59,140,29,50), self.get_images(98, 20, 29, 50),self.get_images(137, 20, 29, 50),
                          self.get_images(176,20,29,50), self.get_images(98, 80, 29, 50),self.get_images(98, 140, 29, 50),
                          self.get_images(137, 80, 29, 50)]
        self.walkLeft = []
        for pic in self.walkRight:
            pic.set_colorkey((0,0,0))
            self.walkLeft.append(pygame.transform.flip(pic, True, False))
        self.jumpSprite = []

    def getX(self):
        return self.rect.left
        
    def getY(self):
        return self.rect.top
        
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
            
            if self.rect.colliderect(platform.collisionRect):
                #left
                if self.vel.x > 0:
                    self.position.x = platform.collisionRect.left - (self.width/2)
                    self.vel.x = 0
                #right
                elif self.vel.x < 0:
                    self.position.x = platform.collisionRect.right + (self.width/2)
                    self.vel.x = 0
                        
    def hitY(self):
        for platform in self.platforms:
            #hit = self.rect.colliderect(platform)
            
            if self.rect.colliderect(platform.collisionRect):
                #top
                if self.vel.y > 0:
                    self.position.y = platform.collisionRect.top
                    self.vel.y = 0
                #bottom
                elif self.vel.y < 0:
                    self.position.y = platform.collisionRect.bottom + self.height
                    self.vel.y = 0
                    
    def checkSpiderCollide(self,spider):
    	#print("testing")
    	#print(spider.get_rect())
    	if spider != None:
    		if self.rect.colliderect(spider.get_rect()):
    			return True
    	return False
    	
    def getKey(self):
    	return self.k	
    	
    def hasKey(self):
    	return self.hasKey
    	
    def update(self, spider = None):
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
        self.lightRect.center = self.position
        if spider != None and self.hasKey == False:
        	keyAppear = self.checkSpiderCollide(spider)
        	if keyAppear:
        		self.k.appearKey(spider)
        		for p in self.platforms:
        			if self.k.rect.colliderect(p):
        				self.k.getRect().bottom = p.rect.top + 20
        		spider.collideSpider()
        		spider.rect.x = -100
        		spider.rect.y = -100
        		#self.hasKey = True
        if self.k.getVis():
        	self.collideKey()
        		
        		
    def collideKey(self):
    	if self.rect.colliderect(self.k.rect):
    		self.k.collidePlayer()
    		self.hasKey = True
    		
		
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
                    self.isRight = True
                if self.vel.x < 0:
                    self.currentSprite = (self.currentSprite+1)%len(self.walkLeft)
                    self.image = self.walkLeft[self.currentSprite]
                    self.isRight = False
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.walking and not self.isJump:
            if nowTicks - self.lastTicks > 500:
                if self.isRight == True:
                    self.lastTicks = nowTicks
                    self.currentSprite = (self.currentSprite+1)% len(self.standingRight)
                    bottom = self.rect.bottom
                    self.image = self.standingRight[self.currentSprite]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                else:
                    self.lastTicks = nowTicks
                    self.currentSprite = (self.currentSprite+1)% len(self.standingLeft)
                    bottom = self.rect.bottom
                    self.image = self.standingLeft[self.currentSprite]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
