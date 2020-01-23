import pygame 
from lighting import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, width = 30, height = 50, mass = 1):
		pygame.sprite.Sprite.__init__(self)
		self.currentSprite = 0
		self.lastTicks = 0
		self.isJump = False
		self.walking = False
		self.load_images()
		self.image = self.standing[0]
		self.rect = self.image.get_rect()
		#self.rect.center = (x, y)
		self.lightRect = lightAlpha.get_rect()
		#self.lightRect.center = (x,y)
		self.width = width
		self.height = height 
		self.mass = mass
		self.vel = vec(0,0)
		self.acc = vec(0,0) 
		self.position = vec(200, 200)
#		self.walkRight = [pygame.image.load(pygame.path.join('',''))]
#		self.walkLeft = []
	
	def get_images(self, a, b, wid, hei):
		sprite = pygame.image.load('Assets/Attempt1.png').convert()
		getimage = pygame.Surface((wid,hei))
		getimage.blit(sprite,(0,0),(a,b,wid,hei))
		getimage = pygame.transform.scale(getimage,(wid, hei))
		return getimage

	def load_images(self):
		self.standing = [self.get_images(20, 20, 32, 52), self.get_images(20, 20, 32, 52)]
		for pic in self.standing:
			pic.set_colorkey((0,0,0))
		self.walkLeft = [self.get_images(20, 82, 32, 52), self.get_images(20, 144, 32, 52)]
		for pic in self.walkLeft:
			pic.set_colorkey((0,0,0))
		self.walkRight = [self.get_images(20, 82, 32, 52), self.get_images(20, 144, 32, 52)]
		for pic in self.walkRight:
			pic.set_colorkey((0,0,0))
		self.jumpSprite = []

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
		self.motion()
		self.acc = vec(0,0)
#		self.vel.x = 0
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			if self.position.x < 10:
				self.acc.x = 0
				self.vel.x = 0
			else:
				self.acc.x = -1
		if keys[pygame.K_RIGHT]:
			if self.position.x > 790:
				self.acc.x = 0
				self.vel.x = 0
			else:
				self.acc.x = 1
		self.acc.x += self.vel.x*(-0.1)
		self.vel += self.acc
		if abs(self.vel.x) < 1:
			self.vel.x = 0 
		self.position += self.vel + 0.5*self.acc
		self.rect.midbottom = self.position

	def motion(self):
		nowTicks = pygame.time.get_ticks()
		if self.vel.x != 0:
			self.walking = True
		else:
			self.walking = False
		if self.walking:
			if nowTicks - self.lastTicks > 300:
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
		self.lightRect.center = self.rect.center
