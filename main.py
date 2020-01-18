# Matthew Maring
# 1/13/2020
# Shadow Puppets Project

import pygame
from pygame import gfxdraw

# Import all the other classes here
#from player import Player

##################################################
##################################################
# SETUP
##################################################

pygame.init()

# Setup the window
logo = pygame.image.load("logo32x32.png")
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

# music setup
pygame.mixer.init()
pygame.mixer.music.load('Window_Demons.ogg')
pygame.mixer.music.play()

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
def button(message, x, y, textColor, initColor, highColor, font, action, level=None):
    text = font.render(message, True, textColor, initColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Action if clicked
    if textRect.right + 7 > mouse[0] > textRect.left - 5 and textRect.bottom + 6 > mouse[1] > textRect.top - 5:
        text = font.render(message, True, textColor, highColor)
        roundCorners(textRect, highColor)

        if click[0] == 1:
            if level != None:
                action(level)
            else:
                action()
    else:
        text = font.render(message, True, textColor, initColor)
        roundCorners(textRect, initColor)

    screen.blit(text, textRect) 
    
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
        
        bg = pygame.image.load("Cave.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Shadow Puppets', 400, 300, white, fontBig)
        
        # button control
        button('Start', 150, 400, white, grey, light_grey, fontBig, levelManager)
        button('Instructions', 325, 400, white, grey, light_grey, fontBig, instructions)
        button('Credits', 522, 400, white, grey, light_grey, fontBig, credits)
        button('Quit', 654, 400, white, grey, light_grey, fontBig, quit)
    
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
        
        bg = pygame.image.load("Cave.png")
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
        
        bg = pygame.image.load("Cave.png")
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
        pygame.mixer.music.load('Window_Demons.ogg')
        pygame.mixer.music.play()
     
    while running:
    
        screen.fill(black) 
        
        bg = pygame.image.load("Cave.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Level #{}'.format(number), 400, 300, white, fontBig)
        
        if score != None:
            label('Current Score: {}'.format(score), 400, 345, white, fontSmall)
        
        # button control
        button('Begin', 400, 400, white, grey, light_grey, fontBig, level, number)
    
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

def level(number):

    running = True
    win = None
    score = 0
    max_levels = 1 # change when we add more levels
    level_time = 30.0 #seconds
    start_time = pygame.time.get_ticks()
    
    # Player init
#     player = Player(screen, 300, 200)
    
    # Lighting init
    
    # Enemy AI init
    
    # Collision init
    
    # Sound init
    pygame.mixer.music.stop() #stop background audio
#     pygame.mixer.music.load('Window_Demons.ogg')
#     pygame.mixer.music.play()
    
    
    ####
    # Main Loop
    ####
    
    while running:
    
        ####
        # Initialize the window
        ####
    
        screen.fill(black)
        
        ####
        # Timer
        ####
        
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        countdown_time = level_time - current_time
        
        time_min = int(countdown_time / 60.0)
        time_sec_int = int(countdown_time) % 60
        time_mili = round(countdown_time % 60.0, 1)
        
        if countdown_time > 10.0 and time_sec_int > 9:
            label('{}:{}'.format(time_min, time_sec_int), 750, 575, white, fontSmall)
        elif countdown_time > 10.0 and time_sec_int < 10:
            label('{}:0{}'.format(time_min, time_sec_int), 750, 575, white, fontSmall)
        elif countdown_time > 5:
            label('{}:0{}'.format(time_min, time_mili), 750, 575, yellow, fontSmall)
        elif countdown_time > 0:
            label('{}:0{}'.format(time_min, time_mili), 750, 575, red, fontSmall)
        else:
            win = False
        
        ####
        #GAME GOES HERE :)
        ####
        
        # Player Control
#         key = pygame.key.get_pressed()
#         if key[pygame.K_LEFT] and player.getX() > player.getVel():
#             player.moveLeft()
#         if key[pygame.K_RIGHT] and player.getX() < 800 - player.getWidth() - player.getVel():
#             player.moveRight()
#         else:
#             player.stand()
#         if key[pygame.K_SPACE]:
#             player.jumpCheck()
#         
#         player.jump()
#         player.draw()
        
        # Lighting Control
        
        
        # Enemy AI Control
        
        
        # Collision Control
        
        
        # Sound Control
        
        
        ####
        # Handle next round
        ####
        
        if win == True and number < max_levels:
            levelManager(win, score, number) #for more than 1 level
        elif win == False:
            endScreen(win, score, number)
            
        ####
        # If quit
        ####
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()

##################################################
##################################################
# END SCREEN
##################################################

def endScreen(win, score, level):
    
    running = True
    
    # Sound init
    pygame.mixer.music.load('Window_Demons.ogg')
    pygame.mixer.music.play()
    
    while running:
    
        screen.fill(black)
        
        bg = pygame.image.load("Cave.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Game Over', 400, 300, white, fontBig)
        
        if win == True:
            label('You won! Your score was {} through level {}'.format(score, level), 400, 375, white, fontSmall)
        else:
            label('You failed, try again! Your score was {} through level {}'.format(score, level), 400, 375, white, fontSmall)
        
        # button control
        if win == True:
            button('Play again', 135, 550, white, grey, light_grey, fontBig, startScreen)
        else:
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
    