import pygame

class Player:
	def __init__(self, win, x, y, width=30, height=50, mass=1):
		self.x = x
		self.y = y
		self.win = win
		self.width = width
		self.height = height
		self.vel = 5
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

	run = True
	while run:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and player.getX()>player.getVel():
			player.moveLeft()
		if key[pygame.K_RIGHT] and player.getX()<screenWidth-player.getWidth()-player.getVel():
			player.moveRight()
		else:
			player.stand()
		if key[pygame.K_SPACE]:
			player.jump()

		win.fill((0,0,0))
		player.draw()
		pygame.display.update()
	pygame.quit()
if __name__ == "__main__":
    main()