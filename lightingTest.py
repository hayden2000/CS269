# Bruce A. Maxwell
# January 2015
#
# Pygame Tutorial Example 3
#
# Creates a scene with many spiders and lets the user brush them away
# with the broom.
#

####################### Setup #########################
# useful imports
import sys
import random

# import pygame
import pygame

# initialize pygame
pygame.init()

# initialize the fonts
try:
	pygame.font.init()
except:
	print "Fonts unavailable"
	sys.exit()

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

# create a font
afont = pygame.font.SysFont( "Helvetica", 20, bold=True )

# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )


####################### Filling the Screen #########################

# A function that draws all of the static background elements
def drawBkg(screen, text, refresh, rect=None):
	# clear the screen with black
	if rect == None:
		screen.fill( (255, 255, 255) )

		# blit the text surface onto the screen
		screen.blit( text, (10, 10) )

		refresh.append( screen.get_rect() )
	else:
		screen.fill( (255, 255, 255), rect )

		# blit the text surface onto the screen if it is inside the rectangle
		screen.fill( (255, 255, 255), text.get_rect().move(10, 10).clip( rect ) )

		trect = text.get_rect().move(10, 10) # rectangle in which to
											 # draw the text
										 
		clippedRect = trect.clip( rect ) # intersection of the text
										 # screen rectangle and the
										 # area to update

		# blit the text into the area to update, the second rectangle
		# indicates which part of the text to use
		urect = screen.blit( text, clippedRect, clippedRect.move(-10,-10) )

		# refresh the rectangle
		refresh.append( rect )
		
		
########## Classes for the lamp posts and lighting system ###########

class Lighting:

	def __init__( self ):
		pass
	
	# Render the area illuminated by stationary lamps
	def renderLamps(self, screen, text, refresh, lampList, spiderList):
		
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
				drawBkg( screen, text, refresh, lamp.lightRect )
				
				# Draw the portions of the lampposts illuminated by light rectangles
				for item in lampList:
					if item.imageRect.colliderect( lamp.lightRect ):
						trect = item.imageRect.clip( lamp.lightRect )
						screen.blit( lampImage, trect, trect.move(-item.imageRect.left,-item.imageRect.top) )
			
				# Draw the portions of the spiders inside the light rectangle
				for item in spiderList:
					if item.colliderect( lamp.lightRect ):
						trect = item.clip( lamp.lightRect )
						screen.blit( spider, trect, trect.move(-item.left,-item.top) )
			
				# Draw the light map onto the screen
				screen.blit( night, lamp.lightRect, lamp.lightRect, special_flags = pygame.BLEND_MULT )
				refresh.append( lamp.lightRect )


	# Render the light rectangle surrounding the player
	def renderPlayer(self, screen, text, refresh, player, lampList, spiderList):
	
		# Erase the area covered by the player light
		drawBkg( screen, text, refresh, player.lightRect )
		
		# Draw the portions of the lampposts illuminated by light rectangles
		for item in lampList:
			if item.imageRect.colliderect( player.lightRect ):
				trect = item.imageRect.clip( player.lightRect )
				screen.blit( lampImage, trect, trect.move(-item.imageRect.left,-item.imageRect.top) )
		
		# Draw the portions of the spiders inside the light rectangle
		for item in spiderList:
			if item.colliderect( player.lightRect ):
				trect = item.clip( player.lightRect )
				screen.blit( spider, trect, trect.move(-item.left,-item.top) )
		
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

	def __init__( self, center, image, lightImage, isLit = False ):
		self.coors = center
		self.lightImage = lightImage
		self.image = image
		
		trect = image.get_rect()
		self.imageRect = trect.move( self.coors[0] - trect.width/2, self.coors[1] - trect.width/2 )
		
		trect = lightImage.get_rect()
		self.lightRect = trect.move( self.coors[0] - trect.width/2, self.coors[1] - trect.width/2 )
		
		self.isLit = isLit
		self.recentFlip = False
		
	def turnOn( self ):
		self.isLit = True
	
	def turnOff( self ):
		self.isLit = False
	
	def checkStatus( self, collisionRect ):
		if collisionRect.colliderect( self.imageRect ) and self.recentFlip == False:
			self.isLit = not self.isLit
			self.recentFlip = True
			if self.isLit == False:
				screen.fill( (0,0,0), self.lightRect  )
		if collisionRect.colliderect( self.imageRect ) == False and self.recentFlip:
			self.recentFlip = False
		
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
		


############## Setting up the Broom as a sprite ################

# get the current mouse information, and make the cursor invisible if
# it is focused on the game window
pygame.event.pump()
if pygame.mouse.get_focused():
	pygame.mouse.set_visible(False)

# get the mouse position and put the broom so it is centered on the
# mouse location
tpos = pygame.mouse.get_pos()
trect = broom.get_rect()
broomRect = broom.get_rect().move( tpos[0] - trect.width/2, tpos[1] - trect.height/2 )
broomActiveRect = pygame.Rect((4, 41),(106, 82))

# get the light rectangle centered on the mouse
trect = lightAlpha.get_rect()
lightActiveRect = lightAlpha.get_rect().move( tpos[0] - trect.width/2, tpos[1] - trect.height/2 )

# Create mouse object
player = Player( broom, broomRect, broomActiveRect, lightActiveRect )

# instantiate lighting class
lighting = Lighting()

# Create a list of lamp object
lampList = [ Lamp( (150,300), lampImage, lightAlpha, False ), Lamp( (150,150), lampImage, lightAlpha, True ) ]

####################### Set up the spiders #####################

MaxSpiders = 5
MinSpawnTime = 30

# store a list of rectangles of the active spiders
activeSpiders = []
ticksSinceLastSpawn = 0

####################### Main Event Loop #########################
# set up the refresh rectangle container
refresh = []
screen.fill( (0, 0, 0) )

# Draw background illuminated by lights, then render light/darkness on top
#lighting.drawBkg( screen, text, refresh, lightActiveRect, lampList )
lighting.renderLamps( screen, text, refresh, lampList, activeSpiders )

# update the display before we start the main loop
pygame.display.update()

# respond to mouse motion events until someone clicks a mouse or hits a key
print "Entering main loop"
while 1:

	# handle events and erase things
	for event in pygame.event.get():
		if event.type == pygame.MOUSEMOTION:
			# erase the existing broom
			screen.fill( (0,0,0), player.lightRect )
			refresh.append( player.lightRect )
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			sys.exit()

		if event.type == pygame.QUIT:
			sys.exit()

	# see if we need to add a spider
	if len( activeSpiders ) < MaxSpiders and ticksSinceLastSpawn > MinSpawnTime:

		# 10% chance per tick of a spawn
		if random.random() < 0.1:
			# pick a random location and add a new spider to the list
			tx = random.randint( 10, 560 )
			ty = random.randint( 40, 400 )
			trect = spider.get_rect().move( tx, ty )
			activeSpiders.append( trect )

			# reset ticks since last spawn
			ticksSinceLastSpawn = 0

	ticksSinceLastSpawn += 1

	# draw the background behind each of the spiders
	# this is erasing stuff
	for item in activeSpiders:
		screen.fill( (0, 0, 0), item )
		refresh.append( item )

	# If the game is in focus, update mouse position
	if pygame.mouse.get_focused():
		pygame.mouse.set_visible(False)
		tpos = pygame.mouse.get_pos()

		# update the position of the cursor
		player.updateCoors( tpos[0], tpos[1] )
		
	else:
		pygame.mouse.set_visible(True)

	# figure out if the broom is intersecting any of the spiders
	tmpactive = []
	for item in activeSpiders:
		spiderCollisionBox = spiderActiveRect.move( item.left, item.top )
		if player.collisionRect.colliderect( spiderCollisionBox ):
			continue
		else:
			tmpactive.append( item )
	activeSpiders = tmpactive
	
	for lamp in lampList:
		lamp.checkStatus( player.collisionRect )
			

	# Render everything to the screen
	lighting.renderLamps( screen, text, refresh, lampList, activeSpiders )
	lighting.renderPlayer( screen, text, refresh, player, lampList, activeSpiders )

	# update the parts of the screen that need it
	pygame.display.update( refresh )

	# clear out the refresh rects
	refresh = []

	# throttle the game speed to 30fps
	gameClock.tick(30)
        
# done
print "Terminating"
