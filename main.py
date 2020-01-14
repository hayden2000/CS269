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
def button(message, x, y, textColor, initColor, highColor, font, action):
    text = font.render(message, True, textColor, initColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Action if clicked
    if textRect.right > mouse[0] > textRect.left and textRect.bottom > mouse[1] > textRect.top:
        text = font.render(message, True, textColor, highColor)

        if click[0] == 1:
            action()
    else:
        text = font.render(message, True, textColor, initColor)

    screen.blit(text, textRect) 
    
##################################################
##################################################
# START SCREEEN
##################################################

def startScreen():

    running = True
     
    while running:
    
        screen.fill(black) 
  
        # label control 
        label('Shadow Puppets', 400, 300, white, fontBig)
        
        # button control
        button(' Start ', 100, 400, white, grey, light_grey, fontBig, level1)
        button(' Instructions ', 300, 400, white, grey, light_grey, fontBig, instructions)
        button(' Credits ', 550, 400, white, grey, light_grey, fontBig, credits)
        button(' Quit ', 700, 400, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################  
##################################################
# INSTRUCTION SCREEEN
##################################################
    
def instructions():

    running = True
    
    while running:

        screen.fill(black) 
  
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
# CRTEDITS SCREEEN
##################################################
    
def credits():

    running = True
    
    while running:
    
        screen.fill(black)
  
        # label control 
        label('Credits - Shadow Puppets', 400, 50, white, fontBig)
        
        label('Producer - Sawyer Strong', 400, 100, white, fontSmall)
        label('Designer - Brendan Martin', 400, 150, white, fontSmall)
        label('Lead Programmers - Natalie Lunbeck and Matthew Maring', 400, 200, white, fontSmall)
        label('Lead Visual Artists - Changling Li and Alaleh Naderi', 400, 250, white, fontSmall)
        label('Lead Audio Artists - Chris Shaffrey', 400, 300, white, fontSmall)
        label('Lead QA - Changling Li', 400, 350, white, fontSmall)
        
        label('Colby College, 2020 Jan Plan, CS269 Game Design', 400, 425, white, fontSmall)
        
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
# TEMP LEVEL 1 SCREEEN
##################################################
    
def level1():
    newLevelNotifier(1)
    endScreen()
    
##################################################    
##################################################
# NEW LEVEL SCREEEN
##################################################
    
def newLevelNotifier(number):
    pass
    
##################################################    
##################################################
# GENERIC LEVEL SCREEEN
##################################################

#to be implemented in later revisions of the game

##################################################
##################################################
# END SCREEEN
##################################################

def endScreen():
    pass
    
##################################################    
##################################################
# NOW LET'S RUN IT :)
##################################################

if __name__=="__main__":
    startScreen()
    