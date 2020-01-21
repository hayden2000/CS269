#init
character = Player(200,200)
playing = True





#main loop
all_sprites.update()
all_sprites.draw(screen)



if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_SPACE:
		character.jumpCheck()
		character.jump()
		
		
		
		
		

			self.events()
			self.update()
			self.draw()

	def update(self):
		self.

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			

	def draw(self):
		self.screen.fill((255,255,255))
		
		pygame.display.flip()

def main():
	pygame.init()
	g = Game()
	while g.getRunning():
		
	pygame.quit()
if __name__ == '__main__':
	main()



	