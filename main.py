# Matthew Maring
# 1/13/2020
# Shadow Puppets Project, CS267

# lighting by Brendan Martin
# enemy-ai by
# collision by 
# player by
# sounds by
# art by
# infrastructure see above

##################################################

import pygame, sys, random, os, numpy
from pygame import gfxdraw

# Import all the other classes here
from player import *
#from collision import
from spiderTesting import *
from lighting import *
from Block import *

##################################################
##################################################
# SETUP
##################################################

#os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)

pygame.init()

# Setup the window
logo = pygame.image.load("Assets/logo32x32.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Shadow Puppets")
screen = pygame.display.set_mode((800,600))

# color schemes - changes everywhere :)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (127, 127, 127)
light_grey = (200, 200, 200)
fontBig = pygame.font.Font('freesansbold.ttf', 32)
fontSmall = pygame.font.Font('freesansbold.ttf', 20)

# clock
gameClock = pygame.time.Clock()

# music setup
pygame.mixer.init()
pygame.mixer.music.load('Audio/BACKGROUND.ogg')
pygame.mixer.music.play(-1)

##################################################
##################################################
# UI COMPONENT FUNCTIONS
##################################################

# Define a label for the view
def label(message, x, y, textColor, font):
    text = font.render(message, True, textColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    screen.blit(text, textRect)

# Define a button for the view
def button(message, x, y, textColor, initColor, highColor, font, action, level=None, number=None):
    text = font.render(message, True, textColor, initColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    mouse = pygame.mouse.get_pos()
    
    # Action if clicked
    if textRect.right + 7 > mouse[0] > textRect.left - 5 and textRect.bottom + 6 > mouse[1] > textRect.top - 5:
        text = font.render(message, True, textColor, highColor)
        roundCorners(textRect, highColor)
        
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                clicked = True

        if clicked == True:
            clicked = False
            if level != None and number != None:
                action(level, number)
            elif level != None:
                action(level)
            else:
                action()
    else:
        text = font.render(message, True, textColor, initColor)
        roundCorners(textRect, initColor)

    screen.blit(text, textRect) 
    
def image(pic, x, y, w, h):
    bg = pygame.image.load("Assets/{}.png".format(pic))
    bg = pygame.transform.scale(bg, (w, h))
    screen.blit(bg, (x, y))
    
def roundCorners(textRect, color):
    # Get the corners of the buttons
    x0, y0 = textRect.topleft
    x1, y1 = textRect.topright
    x2, y2 = textRect.bottomleft
    x3, y3 = textRect.bottomright
    
    # Adjust sizes to center text
    y2 = y2 - 3
    y3 = y3 - 3
    
    # Draw the arcs for each button
    gfxdraw.aacircle(screen, x0, y0, 5, color)
    gfxdraw.filled_circle(screen, x0, y0, 5, color)
    
    gfxdraw.aacircle(screen, x1, y1, 5, color)
    gfxdraw.filled_circle(screen, x1, y1, 5, color)
    
    gfxdraw.aacircle(screen, x2, y2, 5, color)
    gfxdraw.filled_circle(screen, x2, y2, 5, color)
    
    gfxdraw.aacircle(screen, x3, y3, 5, color)
    gfxdraw.filled_circle(screen, x3, y3, 5, color)
    
    # Extend the size of each button to smooth the corners
    gfxdraw.box(screen, pygame.Rect(x0, y0 - 5, x1 - x0, 5), color)
    gfxdraw.box(screen, pygame.Rect(x1, y1, 6, y3 - y1), color)
    gfxdraw.box(screen, pygame.Rect(x2, y2, x3 - x2, 6), color)
    gfxdraw.box(screen, pygame.Rect(x0 - 5, y0, 5, y2 - y0), color)
    
##################################################
##################################################
# START SCREEN
##################################################

def startScreen():

    running = True
     
    while running:
    
        screen.fill(black) 
        
        bg = pygame.image.load("Assets/StartScreen.png")
        screen.blit(bg, (0, 0))
        
        # button control
        button('Start', 150, 450, white, grey, light_grey, fontBig, storyManager)
        button('Instructions', 325, 450, white, grey, light_grey, fontBig, instructions)
        button('Credits', 522, 450, white, grey, light_grey, fontBig, credits)
        button('Quit', 654, 450, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################  
##################################################
# INSTRUCTION SCREEN
##################################################
    
def instructions():

    running = True
    
    while running:

        screen.fill(black)

        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0)) 
  
        # label control 
        label('Instructions - Shadow Puppets', 400, 50, white, fontBig)
        
        # button control
        button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
        button('Quit', 700, 550, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################  
##################################################
# CRTEDITS SCREEN
##################################################
    
def credits():

    running = True
    
    while running:
    
        screen.fill(black)
        
        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Credits - Shadow Puppets', 400, 50, white, fontBig)
        
        label('Producer - Sawyer Strong', 400, 125, white, fontSmall)
        label('Designer - Brendan Martin', 400, 175, white, fontSmall)
        label('Lead Programmers - Natalie Lunbeck and Matthew Maring', 400, 225, white, fontSmall)
        label('Lead Visual Artists - Changling Li and Alaleh Naderi', 400, 275, white, fontSmall)
        label('Lead Audio Artist - Chris Shaffrey', 400, 325, white, fontSmall)
        label('Lead QA - Changling Li', 400, 375, white, fontSmall)
        
        label('Colby College, 2020 Jan Plan, CS269 Game Design', 400, 475, white, fontSmall)
        
        # button control
        button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
        button('Quit', 700, 550, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# STORY MANAGER
##################################################
    
def storyManager(page=None):
    
    if page != None:
        story(page)
    else:
        story(1)
    
##################################################  
##################################################
# STORY SCREEN
##################################################
    
def story(page=None):

    running = True
    numberOfPages = 3
    
    while running:

        screen.fill(black)

        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0)) 
        
        if page == 1:
            image('cat1', 100, 100, 600, 400)
        elif page == 2:
            image('cat2', 100, 100, 600, 400)
        else:
            image('cat3', 100, 100, 600, 400)
        
        # button control
        if page == 1:
            button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
        else:
            button('Back', 100, 550, white, grey, light_grey, fontBig, story, page-1)
        
        button('Skip', 700, 50, white, grey, light_grey, fontBig, levelManager)   
        
        if page < numberOfPages:
            button('Next', 700, 550, white, grey, light_grey, fontBig, story, page+1)
        else:
            button('Start', 700, 550, white, grey, light_grey, fontBig, levelManager)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# LEVEL MANAGER
##################################################
    
def levelManager(willContinue=None, score=None, level=None):
    
    if willContinue != None:
        newLevelNotifier(level + 1, score)
    else:
        newLevelNotifier(1)
    
##################################################    
##################################################
# NEW LEVEL SCREEEN
##################################################
    
def newLevelNotifier(number, score=None):
    
    running = True
    
    if score != None:
        # Sound init
        pygame.mixer.music.load('Audio/BACKGROUND.ogg')
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
     
    while running:
    
        screen.fill(black) 
        
        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Level #{}'.format(number), 400, 300, white, fontBig)
        
        if score != None:
            label('Current Score: {}'.format(score), 400, 345, white, fontSmall)
        
        # button control
        button('Begin', 400, 400, white, grey, light_grey, fontBig, level, number, score)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# GENERIC LEVEL SCREEN
##################################################

def level(number, score=None):

    running = True
    win = None
    if score == None:
        score = 0
    max_levels = 2 # change when we add more levels
    level_time = 30.0 #seconds
    start_time = pygame.time.get_ticks()
    
    ##################################################
    # Player init
    ##################################################
    
    platforms = layout_level1(screen)
    
    #Layout(number, screen)
    Layout(1, screen)
    
    player = Player(200,200,platforms)
    
    ##################################################
    # Lighting init
    ##################################################
    
    # get the current mouse information, and make the cursor invisible if
    # it is focused on the game window
    pygame.event.pump()
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)

    # instantiate lighting class
    lighting = Lighting()

    # Create a list of lamp object
    lampList = [ Lamp( (150,150), lampImage, lightAlpha, 5 ), Lamp( (650,150), lampImage, lightAlpha, 5 ), Lamp( (150,450), lampImage, lightAlpha, 5 ), Lamp( (650,450), lampImage, lightAlpha, 5 ) ]

    # set up the refresh rectangle container
    refresh = []
    screen.fill(black)

    # Draw background illuminated by lights, then render light/darkness on top
    lighting.renderLamps( screen, refresh, lampList, platforms )
    
    ##################################################
    # Enemy AI init
    ##################################################

    #spider comes in during last level
    
    spider = None
    
    if number == max_levels:
        spider_img = pygame.image.load("Assets/Spider.png").convert_alpha()
        spider = Enemy(screen, 300, 500, spider_img)
        frame = 0
    
    ##################################################
    # Sound init
    ##################################################

    pygame.mixer.music.stop() #stop background audio
    pygame.mixer.music.load('Audio/OPTION2.ogg')
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
    
    ####
    # Main Loop :)
    ####
    
    while running:
    
        ####
        # Initialize the window
        ####
    
        screen.fill(black)
        
        #bg = pygame.image.load("Assets/Cave.png")
        #screen.blit(bg, (0, 0))
        
        ####
        # Timer
        ####
        
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        countdown_time = level_time - current_time
        
        time_min = int(countdown_time / 60.0)
        time_sec_int = int(countdown_time) % 60
        time_mili = round(countdown_time % 60.0, 1)
        
        if countdown_time > 10.0 and time_sec_int > 9:
        	text = fontSmall.render('{}:{}'.format(time_min, time_sec_int), True, white)
        	textRect = text.get_rect()
        	textRect.center = (750, 575)
        elif countdown_time > 10.0 and time_sec_int < 10:
        	text = fontSmall.render('{}:0{}'.format(time_min, time_sec_int), True, white)
        	textRect = text.get_rect()
        	textRect.center = (750, 575)
        elif countdown_time > 5:
        	text = fontSmall.render('{}:0{}'.format(time_min, time_mili), True, yellow)
        	textRect = text.get_rect()
        	textRect.center = (750, 575)
        elif countdown_time > 0:
        	text = fontSmall.render('{}:0{}'.format(time_min, time_mili), True, red)
        	textRect = text.get_rect()
        	textRect.center = (750, 575)
        else:
            win = False
        
        ####
        #START OF GAME LOGIC :)))))
        ####
        
        ##################################################
        # Player Control
        ##################################################
        # handle events and erase things
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jumpCheck()
                    player.jump()
            if event.type == pygame.QUIT:
                running = False
        
        player.update()
        
        
        ##################################################
        # Enemy AI Control
        ##################################################
        
        if number == max_levels:
            frame += 1
            spider.move(player, frame)
            #spider.draw(screen, spider_img)        
        
        ##################################################
        # Lighting Control
        ##################################################

        # If the game is in focus, update mouse position
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)        
        else:
            pygame.mouse.set_visible(True)
    
        # Check if the player touches any of the lamps
        for lamp in lampList:
            lamp.checkStatus( player.rect )
            
        # Render everything to the screen
        lighting.renderLamps( screen, refresh, lampList, platforms, spider )
        lighting.renderPlayer( screen, refresh, player, lampList, platforms, spider )
        
        # Draw the timer after everything else
        screen.blit(text, textRect)
        refresh.append(textRect)

		# Check if the player has won
        counter = 0
        for lamp in lampList:
            if lamp.isLit:
                counter += 1
        if counter == len(lampList):
            win = True
            
        # score display
        stext = fontSmall.render('{}'.format(counter + score), True, white)
        stextRect = stext.get_rect()
        stextRect.center = (25, 575)
        screen.blit(stext, stextRect)
        refresh.append(stextRect)
        
        # update the parts of the screen that need it
        pygame.display.update(refresh)

        # clear out the refresh rects
        refresh = []

        # throttle the game speed to 30fps
        gameClock.tick(30)
        
        ####
        # Handle next round
        ####
        
        if win != None:
            pygame.mouse.set_visible(True)
            score += counter # update score
                       
            if win == True and number < max_levels:
                levelManager(win, score, number) #for more than 1 level
            else:
                endScreen(win, score, number)
        
        pygame.display.update(refresh)
        #pygame.display.update()
                
    pygame.quit()
    quit()

##################################################
##################################################
# END SCREEN
##################################################

def endScreen(win, score, level):
    
    running = True
    
    # Sound init
    pygame.mixer.music.load('Audio/BACKGROUND.ogg')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    
    while running:
    
        screen.fill(black)

        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0))
  
        # button/label control 
        
        if win == True:
            label('You won!', 400, 300, white, fontBig)
            label('Your score was {} through level {}!'.format(score, level), 400, 375, white, fontSmall)
            
            button('Play again', 135, 550, white, grey, light_grey, fontBig, startScreen)
        else:
            label('Game Over', 400, 300, white, fontBig)
            label('You failed, try again! Your score was {} through level {}.'.format(score, level), 400, 375, white, fontSmall)
        
            button('Try again', 135, 550, white, grey, light_grey, fontBig, startScreen)
 
        button('Quit', 710, 550, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# NOW LET'S RUN IT :)
##################################################

if __name__=="__main__":
    startScreen()
    