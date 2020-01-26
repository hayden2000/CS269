
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
spider_img = pygame.image.load( "Assets/Spider.png" ).convert_alpha()
# spiderActiveRect = pygame.Rect( (1, 41), (124, 73) )

#broom = pygame.image.load( "Assets/Broom.png" ).convert_alpha()
lightAlpha = pygame.image.load( "Assets/lightAlpha.png" ).convert_alpha()
night = pygame.Surface( (width, height) )
lampImage = pygame.image.load( "Assets/lamp.png" ).convert_alpha()

Cave = pygame.image.load( "Assets/CaveContrast.png" ).convert_alpha()

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
	def renderLamps(self, screen, refresh, lampList, platforms, spider = None):
		
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

				# Draw the platforms which intersect the lamp's lighting circle
				for plat in platforms:
					if lamp.lightRect.colliderect( plat.rect ):
 						trect = lamp.lightRect.clip( plat.rect )
 						screen.blit( plat.image, trect, trect.move(-plat.rect.left,-plat.rect.top) )
				
				# Draw the spider enemy
				if spider != None:
					if spider.get_rect().colliderect( lamp.lightRect ):
						# image = spider.draw()
# 						trect = image.get_rect().clip( lamp.lightRect )
# 						screen.blit( image, trect, trect.move( -image.get_rect().left, -image.get_rect().top) )
					 	spider.draw(screen, spider_img)
# 						trect = spider.get_rect().clip( lamp.lightRect )
# 						screen.blit( spider_img, trect, trect.move(-spider.getX(),-spider.getY()) )

				# Draw the light map onto the screen
				screen.blit( night, lamp.lightRect, lamp.lightRect, special_flags = pygame.BLEND_MULT )
				refresh.append( lamp.lightRect )


	# Render the light rectangle surrounding the player
	def renderPlayer(self, screen, refresh, player, lampList, platforms, spider = None):
	
		# Erase the area covered by the player light
		drawBkg( screen, refresh, player.lightRect )
		
		# Draw the portions of the lampposts illuminated by light rectangles
		for item in lampList:
			if item.imageRect.colliderect( player.lightRect ):
				trect = item.imageRect.clip( player.lightRect )
				screen.blit( lampImage, trect, trect.move(-item.imageRect.left,-item.imageRect.top) )

		# Draw the platforms which intersect the player's lighting circle
		for plat in platforms:
			if player.lightRect.colliderect( plat.rect ):
				trect = player.lightRect.clip( plat.rect )
				screen.blit( plat.image, trect, trect.move(-plat.rect.left,-plat.rect.top) )
		
		# Draw the spider enemy
		if spider != None:
			if spider.get_rect().colliderect( player.lightRect ):
			
				# image = spider.draw()
# 				trect = spider.get_rect().clip( player.lightRect )
# 				screen.blit( image, trect, trect.move( -image.get_rect().left, -image.get_rect().top))
				spider.draw(screen, spider_img)
				# trect = spider.get_rect().clip( player.lightRect )
# 				screen.blit( spider_img, trect, trect.move(-spider.getX(),-spider.getY()) )
		
		# Draw the player image
		screen.blit( player.image, player.rect )
		
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

	def __init__( self, midbottom, image, lightImage, timer = -1, isLit = False ):
		self.coors = ( midbottom[0], midbottom[1] - 40 )
		#self.coors[1] = midbottom[1] + ( image.get_rect().height )/2
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
		if collisionRect.colliderect( self.imageRect ) and self.recentFlip == False:
			self.recentFlip = True
			pygame.mixer.init()
			lit=pygame.mixer.Sound('Audio/COMPLETE.ogg')
			lit.set_volume(0.5)
			pygame.mixer.Sound.play(lit)
			self.isLit = True
			self.counter = 0
		elif self.isLit and self.timeLimit >= 0:
			self.recentFlip = False
			if self.counter >= self.timeLimit:
				dim=pygame.mixer.Sound('Audio/Extinguished.ogg')
				dim.set_volume(1)
				pygame.mixer.Sound.play(dim)
				self.counter = 0
				self.isLit = False
				screen.fill( (0,0,0), self.lightRect )
			else:
				self.counter += 1

# Class to represent the playable character
#class Player:
#	
#	def __init__( self, image, imageRect, collisionRect, lightRect ):
#		self.image = image
#		self.imageRect = imageRect
#		self.collisionRect = collisionRect
#		self.lightRect = lightRect
#	
#	# Update the positions of all the rectangles, based on the center coordinates (x,y)
#	def updateCoors( self, x, y ):
#		self.imageRect = pygame.Rect( (x - self.imageRect.width/2, y - self.imageRect.height/2),
#								  (self.imageRect.width, self.imageRect.height) )
#		self.lightRect = pygame.Rect( (x - self.lightRect.width/2, y - self.lightRect.height/2),
#								  (self.lightRect.width, self.lightRect.height) )
#		self.collisionRect.left = self.imageRect.left
#		self.collisionRect.top = self.imageRect.top

############## Setting up the Broom as a sprite ################

# get the current mouse information, and make the cursor invisible if
# it is focused on the game window
# pygame.event.pump()
# if pygame.mouse.get_focused():
# 	pygame.mouse.set_visible(False)
# 
# # get the mouse position and put the broom so it is centered on the
# # mouse location
# tpos = pygame.mouse.get_pos()
# trect = broom.get_rect()
# broomRect = broom.get_rect().move( tpos[0] - trect.width/2, tpos[1] - trect.height/2 )
# broomActiveRect = pygame.Rect((4, 41),(106, 82))
# 
# # get the light rectangle centered on the mouse
# trect = lightAlpha.get_rect()
# lightActiveRect = lightAlpha.get_rect().move( tpos[0] - trect.width/2, tpos[1] - trect.height/2 )
# 
# # Create mouse object
# player = Player( broom, broomRect, broomActiveRect, lightActiveRect )
# 
# # instantiate lighting class
# lighting = Lighting()
# 
# # Create a list of lamp object
# lampList = [ Lamp( (150,300), lampImage, lightAlpha ), Lamp( (150,150), lampImage, lightAlpha, -5, False ) ]
# 
# ####################### Main Event Loop #########################
# # set up the refresh rectangle container
# refresh = []
# screen.fill( (0, 0, 0) )
# 
# # Draw background illuminated by lights, then render light/darkness on top
# #lighting.drawBkg( screen, text, refresh, lightActiveRect, lampList )
# lighting.renderLamps( screen, refresh, lampList )
# 
# # update the display before we start the main loop
# pygame.display.update()
# 
# # respond to mouse motion events until someone clicks a mouse or hits a key
# print "Entering main loop"
# while 1:
# 
# 	# handle events and erase things
# 	for event in pygame.event.get():
# 		if event.type == pygame.MOUSEMOTION:
# 			# erase the existing broom
# 			screen.fill( (0,0,0), player.lightRect )
# 			refresh.append( player.lightRect )
# 		
# 		#if event.type == pygame.MOUSEBUTTONDOWN:
# 			#sys.exit()
# 
# 		if event.type == pygame.KEYDOWN:
# 			sys.exit()
# 
# 		if event.type == pygame.QUIT:
# 			sys.exit()
# 
# 
# 	# If the game is in focus, update mouse position
# 	if pygame.mouse.get_focused():
# 		pygame.mouse.set_visible(False)
# 		tpos = pygame.mouse.get_pos()
# 
# 		# update the position of the cursor
# 		player.updateCoors( tpos[0], tpos[1] )
# 		
# 	else:
# 		pygame.mouse.set_visible(True)
# 	
# 	# Check if the player touches any of the lamps
# 	for lamp in lampList:
# 		lamp.checkStatus( player.collisionRect )
# 			
# 
# 	# Render everything to the screen
# 	lighting.renderLamps( screen, refresh, lampList )
# 	lighting.renderPlayer( screen, refresh, player, lampList )
# 
# 	# update the parts of the screen that need it
# 	pygame.display.update( refresh )
# 
# 	# clear out the refresh rects
# 	refresh = []
# 
# 	# throttle the game speed to 30fps
# 	gameClock.tick(30)
#         
# # done
# print "Terminating"
