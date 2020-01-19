import pygame 
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, width = 30, height = 50, mass = 1):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30,50))
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.width = width
		self.height = height 
		self.mass = mass
		self.vel = vec(0,0)
		self.acc = vec(0,0) 
		self.position = vec(x, y)
		self.isJump = False

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
#		self.vel.x = 0
		keys = pygame.key.get_pressed()
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

