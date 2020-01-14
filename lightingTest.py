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
import copy

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
#pygame.image.load( "night.png" ).convert_alpha()

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

class lighting:

	def __init__( self ):
		pass
	
	# Render the area illuminated by stationary lamps
	def renderLamps(self, screen, text, refresh, lampList, spiderList):
		
		# Create light map "night"
		night.fill( (0,0,0) )
		for lamp in lampList:
			night.blit( lightAlpha, lamp.lightRect )
	
		# For each light rectangle, erase what is there, draw the background
		# then blit the light on top
		for lamp in lampList:
			screen.fill( (0,0,0), lamp.lightRect )
			drawBkg( screen, text, refresh, lamp.lightRect )
			
			for item in spiderList:
				if item.colliderect( lamp.lightRect ):
					trect = item.clip( lamp.lightRect )
					screen.blit( spider, trect, trect.move(-item.left,-item.top) )
			
			screen.blit( night, lamp.lightRect, special_flags = pygame.BLEND_MULT )
			refresh.append( lamp.lightRect )


	# Render the light rectangle surrounding the player
	def renderPlayer(self, screen, text, refresh, PC, lampList, spiderList):
	
		screen.fill( (0,0,0), PC )
		drawBkg( screen, text, refresh, PC )
		
		for item in spiderList:
			if item.colliderect( PC ):
				trect = item.clip( PC )
				drawBkg( screen, text, refresh, trect )
				screen.blit( spider, trect, trect.move(-item.left,-item.top) )
		
		screen.blit( broom, broomRect )
		
		# Create light map "night"
		night.fill( (0,0,0) )
		for lamp in lampList:
			#if PC.colliderect( lamp.lightRect ):
			night.blit( lightAlpha, lamp.lightRect )
		night.blit( lightAlpha, PC )
		
		screen.blit( night, PC, PC, special_flags = pygame.BLEND_MULT )
		refresh.append( PC )
		

class lamp:

	def __init__( self, upperLeft, lightRect ):
		self.lightRect = lightRect
		self.coors = upperLeft


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

# blit the broom to the screen and update the display
screen.blit( broom, broomRect )

# instantiate lighting class
lighting = lighting()

# get the corner lamp
lampList = [ lamp( (0,0), lightAlpha.get_rect() ) ]

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
			screen.fill( (0,0,0), lightActiveRect )
			refresh.append( lightActiveRect )
		
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


	# figure out if the broom is intersecting any of the spiders
	tmpactive = []
	for item in activeSpiders:
		spiderCollisionBox = spiderActiveRect.move( item.left, item.top )
		broomCollisionBox = broomActiveRect.move( broomRect.left, broomRect.top )
		if broomCollisionBox.colliderect( spiderCollisionBox ):
			continue
		else:
			tmpactive.append( item )
	activeSpiders = tmpactive

	# If the game is in focus, update mouse position
	if pygame.mouse.get_focused():
		pygame.mouse.set_visible(False)
		tpos = pygame.mouse.get_pos()

		# update the position of the cursor
		broomRect = pygame.Rect( (tpos[0] - broomRect.width/2, tpos[1] - broomRect.height/2),
								  (broomRect.width, broomRect.height) )
	
		lightActiveRect = pygame.Rect( (tpos[0] - lightActiveRect.width/2, tpos[1] - lightActiveRect.height/2), (lightActiveRect.width, lightActiveRect.height) )
	else:
		pygame.mouse.set_visible(True)

	# Render everything to the screen
	lighting.renderLamps( screen, text, refresh, lampList, activeSpiders )
	lighting.renderPlayer( screen, text, refresh, lightActiveRect, lampList, activeSpiders )

	# update the parts of the screen that need it
	pygame.display.update( refresh )

	# clear out the refresh rects
	refresh = []

	# throttle the game speed to 30fps
	gameClock.tick(30)
        
# done
print "Terminating"
