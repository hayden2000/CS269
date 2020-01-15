# Matthew Maring
# 1/13/2020
# Shadow Puppets Project

import pygame

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
black = (0, 0, 0)
grey = (127, 127, 127)
light_grey = (200, 200, 200)
fontBig = pygame.font.Font('freesansbold.ttf', 32)
fontSmall = pygame.font.Font('freesansbold.ttf', 20)

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
    if textRect.right > mouse[0] > textRect.left and textRect.bottom > mouse[1] > textRect.top:
        text = font.render(message, True, textColor, highColor)

        if click[0] == 1:
            if level != None:
                action(level)
            else:
                action()
    else:
        text = font.render(message, True, textColor, initColor)

    screen.blit(text, textRect) 
    
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
        button(' Start ', 150, 400, white, grey, light_grey, fontBig, levelManager)
        button(' Instructions ', 325, 400, white, grey, light_grey, fontBig, instructions)
        button(' Credits ', 522, 400, white, grey, light_grey, fontBig, credits)
        button(' Quit ', 654, 400, white, grey, light_grey, fontBig, quit)
    
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
        button(' Back ', 100, 550, white, grey, light_grey, fontBig, startScreen)
        button(' Quit ', 700, 550, white, grey, light_grey, fontBig, quit)
    
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
        button(' Back ', 100, 550, white, grey, light_grey, fontBig, startScreen)
        button(' Quit ', 700, 550, white, grey, light_grey, fontBig, quit)
    
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
        newLevelNotifier(level + 1)
    else:
        newLevelNotifier(1)
    
##################################################    
##################################################
# NEW LEVEL SCREEEN
##################################################
    
def newLevelNotifier(number):
    
    running = True
     
    while running:
    
        screen.fill(black) 
        
        bg = pygame.image.load("Cave.png")
        screen.blit(bg, (0, 0))
  
        # label control 
        label('Level #{}'.format(number), 400, 300, white, fontBig)
        
        # button control
        button(' Begin ', 400, 400, white, grey, light_grey, fontBig, level, number)
    
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

    win = False
    score = 0
    max_levels = 10
    
    ####
    #GAME GOES HERE :)
    ####
    
    if win == True and number < max_levels:
        endScreen(win, score, number)
        #levelManager(True, score, number) #for more than 1 level
    else:
        endScreen(win, score, number)

##################################################
##################################################
# END SCREEN
##################################################

def endScreen(win, score, level):
    
    running = True
    
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
            button(' Play again ', 135, 550, white, grey, light_grey, fontBig, startScreen)
        else:
            button(' Try again ', 135, 550, white, grey, light_grey, fontBig, startScreen)
            
        button(' Quit ', 710, 550, white, grey, light_grey, fontBig, quit)
    
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
    