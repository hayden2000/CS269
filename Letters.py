# Brendan Martin
# 1/25/2020
# Shadow Puppets Project, CS267

import pygame

class Letter:

	def __init__( self, text, midbottom ):
		self.image = pygame.transform.scale(text, (700, 500))
		self.rect = pygame.Rect((0,0), (50,50))
		self.rect.midbottom = midbottom
		self.icon = pygame.image.load("Assets/letter_icon.png")
		self.icon = pygame.transform.scale( self.icon, (self.rect.width,self.rect.height) )
		self.letter_closed = False
	
	def checkCollide(self, player):
		return player.rect.colliderect( self.rect )
	
	def drawInstruction(self, screen, font, color):
		text = font.render("Press E", True, color)
		textRect = text.get_rect()
		textRect.center = ( self.rect.centerx, self.rect.top - (textRect.height/2) )
		screen.blit(text, textRect)
	
	# Render the area illuminated by stationary lamps
	def display( self, screen, player, font, color ):
		
		startTime = pygame.time.get_ticks()
		running = False
		
		if player.rect.colliderect( self.rect ):
			running = True
			screen.fill((50,0,0))
			screen.blit(self.image, (50,50))
			text = font.render("Press SPACE", True, color)
			textRect = text.get_rect()
			textRect.center = ( 400, 550 )
			screen.blit(text, textRect)
			pygame.display.update()
		
		while running:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						running = False
						self.letter_closed = True
				if event.type == pygame.QUIT:
					pygame.quit()
		return pygame.time.get_ticks() - startTime