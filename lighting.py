
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

	def renderLamps(self, screen, refresh, player, lampList, platforms, doors, letter = None, spider = None):
		
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
 				
 				# Draw the letter icon
				if letter != None:
					if letter.rect.colliderect( lamp.lightRect ):
						trect = lamp.lightRect.clip( letter.rect )
						screen.blit( letter.icon, trect, trect.move(-letter.rect.left,-letter.rect.top) )
						#pygame.draw.rect( screen, (0,100,0), trect )
				
				
				# Draw the doors
				for door in doors:
					if door.rect.colliderect( lamp.lightRect ):
						trect = door.rect.clip( lamp.lightRect )
						screen.blit( door.image, trect, trect.move(-door.rect.left,-door.rect.top) )
				
				# Draw the spider enemy
				if spider != None:
					if spider.get_rotRect().colliderect( lamp.lightRect ):
 						trect = spider.get_rotRect().clip( lamp.lightRect )
 						#screen.blit( image, trect, trect.move( -image.get_rect().left, -image.get_rect().top) )
 						
 						screen.blit( spider.get_rotImage(), trect, trect.move(-spider.getX(),-spider.getY()) )
						#screen.blit( spider.get_rotImage, spider.get_rect(), spider.get_rotImage().get_rect() )

				key = player.getKey()
				if key.isVisible:
					if lamp.lightRect.colliderect( key.rect ):
 						trect = lamp.lightRect.clip( key.rect )
 						screen.blit( key.image, trect, trect.move(-key.rect.left,-key.rect.top) )

				# Draw the light map onto the screen
				screen.blit( night, lamp.lightRect, lamp.lightRect, special_flags = pygame.BLEND_MULT )
				refresh.append( lamp.lightRect )


	# Render the light rectangle surrounding the player
	def renderPlayer(self, screen, refresh, player, lampList, platforms, doors, letter = None, spider = None):
	
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
		
		# Draw the letter icon
		if letter != None:
			if letter.rect.colliderect( player.lightRect ):
				trect = player.lightRect.clip( letter.rect )
				screen.blit( letter.icon, trect, trect.move(-letter.rect.left,-letter.rect.top) )
				#pygame.draw.rect( screen, (0,100,0), trect )

		# Draw the doors
		for door in doors:
			if door.rect.colliderect( player.lightRect ):
				trect = door.rect.clip( player.lightRect )
				screen.blit( door.image, trect, trect.move(-door.rect.left,-door.rect.top) )

		
		# Draw the spider enemy
		if spider != None:
			if spider.get_rotRect().colliderect( player.lightRect ):
				trect = spider.get_rotRect().clip( player.lightRect )
				screen.blit( spider.get_rotImage(), trect, trect.move(-spider.getX(),-spider.getY()) )
				# image = spider.draw()
# 				trect = spider.get_rect().clip( player.lightRect )
# 				screen.blit( image, trect, trect.move( -image.get_rect().left, -image.get_rect().top))
				#spider.draw(screen)
				# trect = spider.get_rect().clip( player.lightRect )
# 				screen.blit( spider_img, trect, trect.move(-spider.getX(),-spider.getY()) )
		
		key = player.getKey()
		if key.isVisible:
			if player.lightRect.colliderect( key.rect ):
				trect = player.lightRect.clip( key.rect )
				screen.blit( key.image, trect, trect.move(-key.rect.left,-key.rect.top) )
		
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
		
# 	def turnOn( self ):
# 		self.isLit = True
# 	
# 	def turnOff( self ):
# 		self.isLit = False
	
	def checkStatus( self, collisionRect, win ):
		if not win:
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
					self.counter = 0
					self.isLit = False
					screen.fill( (0,0,0), self.lightRect )
				else:
					self.counter += 1
	