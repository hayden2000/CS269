#spidertesting


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
    print ("Fonts unavailable")
    sys.exit()

# create a game clock
gameClock = pygame.time.Clock()


# create a screen (width, height)
screen = pygame.display.set_mode( (640, 480) )

####################### Making Content #########################

# load some images
spider = pygame.image.load( "Spider.png" ).convert_alpha()
spiderActiveRect = pygame.Rect( (1, 41), (124, 73) )

broom = pygame.image.load( "Broom.png" ).convert_alpha()

# create a font
afont = pygame.font.SysFont( "Helvetica", 20, bold=True )

# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

#create a start
state = "start"
####################### Filling the Screen #########################

# A function that draws all of the static background elements
def drawBkg(screen, text, refresh, rect=None):
    # clear the screen with white
    if rect == None:
        screen.fill( (255, 255, 255) )

        # blit the text surface onto the screen
        screen.blit( text, (10, 10) )

        refresh.append( screen.get_rect() )
    else:
        #screen.fill((255, 255, 255), rect)

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


class Enemy:  #Class for Spider character
    def __init__(self,x, y):
        self.image = spider
        self.xPos = x
        self.yPos = y
        #self.trect = self.image.get_rect().move( x, y )

    def random_move(self):
        to_do = 1
    def run_away(self,player_x, player_y):
        to_do = 1


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

# blit the broom to the screen and update the display
screen.blit(broom, broomRect)

####################### Set up the spiders #####################

MaxSpiders = 5
MinSpawnTime = 30


# store a list of rectangles of the active spiders
activeSpiders = []
#ticksSinceLastSpawn = 0
spider = Enemy(random.randint( 10, 560 ),random.randint( 40, 400 ))
activeSpiders.append( spider )
#screen.blit(spider)
####################### Main Event Loop #########################
# set up the refresh rectangle container
refresh = []
drawBkg(screen, text, refresh)

# update the display before we start the main loop
pygame.display.update()

# respond to mouse motion events until someone clicks a mouse or hits a key
print("Entering main loop")
while 1:

    # handle events and erase things
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            # erase the existing broom
            drawBkg(screen, text, refresh, broomRect)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            sys.exit()

        if event.type == pygame.QUIT:
            sys.exit()

        # tx = random.randint( 10, 560 )
        # ty = random.randint( 40, 400 )
        # trect = spider.get_rect().move( tx, ty )
        # activeSpiders.append( trect )

    # draw the background behind each of the spiders
    # this is erasing stuff
    for item in activeSpiders:
        drawBkg(screen, text, refresh, item)

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

    # draw all of the spiders, the rectangle is already on the refresh
    # list from the background draw
    for item in activeSpiders:
        screen.blit( spider, item )
        

    # If the game is in focus, draw things
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        tpos = pygame.mouse.get_pos()

        # update the position of the cursor
        broomRect = pygame.Rect( (tpos[0] - broomRect.width/2, tpos[1] - broomRect.height/2),
                                  (broomRect.width, broomRect.height) )

        # draw the broom in the location of the mouse
        screen.blit(broom, broomRect)

        # add to the refresh list
        refresh.append(broomRect)
    else:
        pygame.mouse.set_visible(True)


    # update the parts of the screen that need it
    pygame.display.update(refresh)

    # clear out the refresh rects
    refresh = []

    # throttle the game speed to 30fps
    gameClock.tick(30)
# done
print("Terminating")
