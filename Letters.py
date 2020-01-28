# Brendan Martin
# 1/25/2020
# Shadow Puppets Project, CS267

import pygame

class Letter:

	def __init__( self, text, rect ):
		self.image = pygame.transform.scale(text, (600, 400))
		self.rect = rect
	
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
			screen.blit(self.image, (100,100))
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
				if event.type == pygame.QUIT:
					pygame.quit()
		return pygame.time.get_ticks() - startTime