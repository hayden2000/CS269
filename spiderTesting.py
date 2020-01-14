#SpiderTesting


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
screen = pygame.display.set_mode( (800, 600) )
####################### Making Content #########################

# load some images
spider = pygame.image.load( "Spider.png" ).convert_alpha()
spiderActiveRect = pygame.Rect( (1, 41), (124, 73) )

broom = pygame.image.load( "Broom.png" ).convert_alpha()

# create a font
afont = pygame.font.SysFont( "Helvetica", 20, bold=True )

# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )


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
        screen.fill((255, 255, 255), rect)

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
        
#class for enemy ai
class Enemy:  #Class for Spider character
    def __init__(self, x, y):
        self.image = spider
        self.xPos = x
        self.yPos = y
        #self.trect = self.image.get_rect().move( x, y )

    def random_move(self):
        to_do = 1
    def run_away(self,player_x, player_y):
        to_do = 1
# get the current mouse information, and make the cursor invisible if
# it is focused on the game window
pygame.event.pump()
if pygame.mouse.get_focused():
    pygame.mouse.set_visible(False)


refresh = []
drawBkg(screen, text, refresh)
enemy_spider = Enemy(random.randint( 10, 770 ),random.randint( 40, 580 ))   
# respond to mouse motion events until someone clicks a mouse or hits a key
print("Entering main loop")
while 1:
     # handle events and erase things
    for event in pygame.event.get():
        # if event.type == pygame.MOUSEMOTION:
        #     # erase the existing broom
        #     drawBkg(screen, text, refresh, broomRect)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            sys.exit()

        if event.type == pygame.QUIT:
            sys.exit()
        
    # update the parts of the screen that need it
    pygame.display.update( refresh )

    # clear out the refresh rects
    refresh = []

    # throttle the game speed to 30fps
    gameClock.tick(30)