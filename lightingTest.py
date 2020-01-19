
####################### Setup #########################
# useful imports
import sys

# import pygame
import pygame

# initialize pygame
pygame.init()

# create a game clock
gameClock = pygame.time.Clock()


# create a screen (width, height)
width = 800
height = 600
screen = pygame.display.set_mode( (width, height) )

####################### Making Content #########################

# load some images
spider = pygame.image.load( "Spider.png" ).convert_alpha()
spiderActiveRect = pygame.Rect( (1, 41), (124, 73) )

broom = pygame.image.load( "Broom.png" ).convert_alpha()
lightAlpha = pygame.image.load( "lightAlpha.png" ).convert_alpha()
night = pygame.Surface( (width, height) )
lampImage = pygame.image.load( "lamp.png" ).convert_alpha()

Cave = pygame.image.load( "Cave.png" ).convert_alpha()

####################### Filling the Screen #########################

# A function that draws all of the static background elements
def drawBkg(screen, refresh, rect=None):
	# clear the screen with black
	if rect == None:
		screen.blit( Cave )

		refresh.append( screen.get_rect() )
	else:
		#screen.fill( (255, 255, 255), rect )
		
		screen.blit( Cave, rect, rect )

		# refresh the rectangle
		refresh.append( rect )
		
		
########## Classes for the lamp posts and lighting system ###########

class Lighting:

	def __init__( self ):
		pass
	
	# Render the area illuminated by stationary lamps
	def renderLamps(self, screen, refresh, lampList):
		
		# Create light map surface "night"
		night.fill( (0,0,0) )
		for lamp in lampList:
			if lamp.isLit == True:
				night.blit( lightAlpha, lamp.lightRect )
	
		# For each light rectangle, erase what is there, draw the background
		# then blit the light on top
		for lamp in lampList:
			if lamp.isLit == True:
				screen.fill( (0,0,0), lamp.lightRect )
				drawBkg( screen, refresh, lamp.lightRect )
				
				# Draw the portions of the lampposts illuminated by light rectangles
				for item in lampList:
					if item.imageRect.colliderect( lamp.lightRect ):
						trect = item.imageRect.clip( lamp.lightRect )
						screen.blit( lampImage, trect, trect.move(-item.imageRect.left,-item.imageRect.top) )
			
				# Draw the portions of the spiders inside the light rectangle
				# for item in spiderList:
# 					if item.colliderect( lamp.lightRect ):
# 						trect = item.clip( lamp.lightRect )
# 						screen.blit( spider, trect, trect.move(-item.left,-item.top) )
			
				# Draw the light map onto the screen
				screen.blit( night, lamp.lightRect, lamp.lightRect, special_flags = pygame.BLEND_MULT )
				refresh.append( lamp.lightRect )


	# Render the light rectangle surrounding the player
	def renderPlayer(self, screen, refresh, player, lampList):
	
		# Erase the area covered by the player light
		drawBkg( screen, refresh, player.lightRect )
		
		# Draw the portions of the lampposts illuminated by light rectangles
		for item in lampList:
			if item.imageRect.colliderect( player.lightRect ):
				trect = item.imageRect.clip( player.lightRect )
				screen.blit( lampImage, trect, trect.move(-item.imageRect.left,-item.imageRect.top) )
		
		# Draw the portions of the spiders inside the light rectangle
		# for item in spiderList:
# 			if item.colliderect( player.lightRect ):
# 				trect = item.clip( player.lightRect )
# 				screen.blit( spider, trect, trect.move(-item.left,-item.top) )
		
		# Draw the player image
		screen.blit( player.image, player.imageRect )
		
		# Create light map "night"
		night.fill( (0,0,0) )
		for lamp in lampList:
			if lamp.isLit == True:
				if player.lightRect.colliderect( lamp.lightRect ):
					night.blit( lightAlpha, lamp.lightRect )
		
		night.blit( lightAlpha, player.lightRect )
		
		# Draw the light map on the screen surrounding the player
		screen.blit( night, player.lightRect, player.lightRect, special_flags = pygame.BLEND_MULT )
		refresh.append( player.lightRect )
		
# Class to represent the stationary lamps
class Lamp:

	def __init__( self, center, image, lightImage, timer = -1, isLit = False ):
		self.coors = center
		self.lightImage = lightImage
		self.image = image
		
		trect = image.get_rect()
		self.imageRect = trect.move( self.coors[0] - trect.width/2, self.coors[1] - trect.width/2 )
		
		trect = lightImage.get_rect()
		self.lightRect = trect.move( self.coors[0] - trect.width/2, self.coors[1] - trect.width/2 )
		
		self.isLit = isLit
		self.recentFlip = False
		self.timeLimit = timer * 30    #Convert from seconds to frames
		self.counter = 0
		
	def turnOn( self ):
		self.isLit = True
	
	def turnOff( self ):
		self.isLit = False
	
	def checkStatus( self, collisionRect ):
		# If the rectangles collide and the lamp has not recently been lit
		if collisionRect.colliderect( self.imageRect ):
			self.isLit = True
			self.counter = 0
		elif self.isLit and self.timeLimit >= 0:
			if self.counter >= self.timeLimit:
				self.counter = 0
				self.isLit = False
				screen.fill( (0,0,0), self.lightRect  )
			else:
				self.counter += 1
		
# Class to represent the playable character
class Player:
	
	def __init__( self, image, imageRect, collisionRect, lightRect ):
		self.image = image
		self.imageRect = imageRect
		self.collisionRect = collisionRect
		self.lightRect = lightRect
	
	# Update the positions of all the rectangles, based on the center coordinates (x,y)
	def updateCoors( self, x, y ):
		self.imageRect = pygame.Rect( (x - self.imageRect.width/2, y - self.imageRect.height/2),
								  (self.imageRect.width, self.imageRect.height) )
		self.lightRect = pygame.Rect( (x - self.lightRect.width/2, y - self.lightRect.height/2),
								  (self.lightRect.width, self.lightRect.height) )
		self.collisionRect.left = self.imageRect.left
		self.collisionRect.top = self.imageRect.top
		