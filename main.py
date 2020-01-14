# Matthew Maring
# 1/13/2020
# Shadow Puppets Project


# import the pygame module, so you can use it
import pygame

# initialize the pygame module
pygame.init()

# load and set the logo
logo = pygame.image.load("logo32x32.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Shadow Puppets")

# create a surface on screen that has the size of 800 x 600
screen = pygame.display.set_mode((800,600))

# color schemes
textColor = (255, 255, 255)
black = (0, 0, 0)
grey = (127, 127, 127)
light_grey = (200, 200, 200)
fontBig = pygame.font.Font('freesansbold.ttf', 32)
fontSmall = pygame.font.Font('freesansbold.ttf', 20)

# Define the label parameters
def label(message, x, y, textColor, font):
    text = font.render(message, True, textColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    screen.blit(text, textRect)

# Define the button parameters
def button(message, x, y, textColor, initColor, highColor, font, action):
    text = font.render(message, True, textColor, initColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if textRect.right > mouse[0] > textRect.left and textRect.bottom > mouse[1] > textRect.top:
        text = font.render(message, True, textColor, highColor)

        if click[0] == 1:
            action()
    else:
        text = font.render(message, True, textColor, initColor)

    screen.blit(text, textRect) 
 
# start screen
def startScreen():

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
    
        # completely fill the surface object 
        # with white color 
        screen.fill(black) 
  
        # label control 
        label('Shadow Puppets', 400, 300, textColor, fontBig)
        
        # button control
        button(' Start ', 100, 400, textColor, grey, light_grey, fontBig, level1)
        button(' Instructions ', 300, 400, textColor, grey, light_grey, fontBig, instructions)
        button(' Credits ', 550, 400, textColor, grey, light_grey, fontBig, credits)
        button(' Quit ', 700, 400, textColor, grey, light_grey, fontBig, quit)
    
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
            pygame.display.update()
                
    pygame.quit()
    quit()
    
    
def instructions():

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
    
        # completely fill the surface object 
        # with white color 
        screen.fill(black) 
  
        # label control 
        label('Instructions - Shadow Puppets', 400, 50, textColor, fontBig)
        
        # button control
        button(' Back ', 100, 550, textColor, grey, light_grey, fontBig, startScreen)
        button(' Quit ', 700, 550, textColor, grey, light_grey, fontBig, quit)
    
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
            pygame.display.update()
                
    pygame.quit()
    quit()
    
def credits():

    # define a variable to control the main loop
    running = True
    
    # main loop
    while running:
    
        # completely fill the surface object 
        # with white color 
        screen.fill(black) 
  
        # label control 
        label('Credits - Shadow Puppets', 400, 50, textColor, fontBig)
        
        label('Producer - Sawyer Strong', 400, 100, textColor, fontSmall)
        label('Designer - Brendan Martin', 400, 150, textColor, fontSmall)
        label('Lead Programmers - Natalie Lunbeck and Matthew Maring', 400, 200, textColor, fontSmall)
        label('Lead Visual Artists - Changling Li and Alaleh Naderi', 400, 250, textColor, fontSmall)
        label('Lead Audio Artists - Chris Shaffrey', 400, 300, textColor, fontSmall)
        label('Lead QA - Changling Li', 400, 350, textColor, fontSmall)
        
        label('Colby College, 2020 Jan Plan, CS269 Game Design', 400, 425, textColor, fontSmall)
        
        # button control
        button(' Back ', 100, 550, textColor, grey, light_grey, fontBig, startScreen)
        button(' Quit ', 700, 550, textColor, grey, light_grey, fontBig, quit)
    
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
            pygame.display.update()
                
    pygame.quit()
    quit()
    
def level1():
    newLevelNotifier(1)
    endScreen()
    
def newLevelNotifier(number):
    pass
    
#After first iteration, making multiple levels
#def level(): 

def endScreen():
    pass
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    startScreen()
    
    