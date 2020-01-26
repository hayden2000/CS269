import pygame
#from player import *
class Key(pygame.sprite.Sprite):
	isVisible = False
	def __init__(self, x_pos, y_pos, size):
		img = pygame.image.load('Assets/key.png')
		self.image = img
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect()
		self.rect.centerx = x_pos
		self.rect.y = y_pos
		self.isVisible = False
		
	def appearKey(self,spider):
		print("key is here")
		self.rect.centerx = spider.getX()
		self.rect.y = spider.getY()
		self.isVisible = True
		
	def collidePlayer(self):
		self.isVisible = False
	
	def draw(self, screen):
		if self.isVisible:
			screen.blit(self.image, int(self.rect.x), int(self.rect.y))
		
		

	
	
		
		
	