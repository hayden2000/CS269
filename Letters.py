# Brendan Martin
# 1/25/2020
# Shadow Puppets Project, CS267

import pygame

class Letter:

	def __init__( self, text, rect ):
		self.text = pygame.transform.scale(text, (600, 400))
		self.rect = rect
	
	# Render the area illuminated by stationary lamps
	def display( self, screen, player ):
		
		startTime = pygame.time.get_ticks()
		running = False
		
		if player.rect.colliderect( self.rect ):
			running = True
			screen.blit(self.text, (100,100))
			pygame.display.update()
		
		while running:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						running = False
				if event.type == pygame.QUIT:
					pygame.quit()
		return pygame.time.get_ticks() - startTime