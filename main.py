# Matthew Maring
# 1/13/2020
# Shadow Puppets Project, CS267

##################################################

# Project credits:
# art by Alaleh Naderi, Changling Li, Natalie Lunbeck, and Matthew Maring
# collision by Natalie Lunbeck and Brendan Martin
# doors/letters/tutorial by Brendan Martim, Sawyer Strong, and Matthew Maring
# enemy-ai by Sawyer Strong
# infrastructure/scoring by Matthew Maring
# lighting by Brendan Martin
# player by Changling Li and Brendan Martin
# sounds by Chris Shaffrey

##################################################

import pygame, sys, random, os, numpy, math
from pygame import gfxdraw

from player import *
from spiderTesting import *
from lighting import *
from Block import *
from Door import *

##################################################
##################################################
# SETUP
##################################################

pygame.init()

# Setup the window
logo = pygame.image.load("Assets/logo32x32.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Shadow Puppets")
screen = pygame.display.set_mode((800,600))

# color schemes - changes everywhere :)
white = (255, 255, 255)
green = (0, 255, 0)
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
        button('Start', 104, 450, white, grey, light_grey, fontBig, storyManager)
        button('Credits', 283, 450, white, grey, light_grey, fontBig, credits)
        button('High Scores', 501, 450, white, grey, light_grey, fontBig, highscores)
        button('Quit', 696, 450, white, grey, light_grey, fontBig, quit)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# TUTORIAL MANAGER
##################################################
    
def tutorialManager(page=None):
    
    if page != None:
        tutorial(page)
    else:
        tutorial(1)
    
##################################################  
##################################################
# TUTORIAL SCREEN
##################################################
    
def tutorial(page=None):

    running = True
    win = None
    numberOfPages = 3
    
    ##################################################
    # Player init
    ##################################################
    
    if page == 1:
        platforms, lampList, doors = layout_level1(screen)
    elif page == 2:
        platforms, lampList, doors = layout_level2(screen)
    elif page == 3:
    	platforms, lampList, doors = layout_level3(screen)
    
    player = Player(doors[0].center[0],doors[0].center[1],platforms)
    
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

    # set up the refresh rectangle container
    refresh = []
    screen.fill(black)

    # Draw background illuminated by lights, then render light/darkness on top
    lighting.renderLamps( screen, refresh, player, lampList, platforms, doors )
    
    ##################################################
    # Sound init
    ##################################################

    pygame.mixer.music.stop() #stop background audio
    pygame.mixer.music.load('Audio/OPTION2.ogg')
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
    
    # Main Loop :)
    while running:

        # Initialize the window
        screen.fill(black)

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
        # Lighting Control
        ##################################################

        # If the game is in focus, update mouse position
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)        
        else:
            pygame.mouse.set_visible(True)
    
        # Check if the player touches any of the lamps
        for lamp in lampList:
            lamp.checkStatus( player.rect, win )
            
        # Render everything to the screen
        lighting.renderLamps( screen, refresh, player, lampList, platforms, doors )
        lighting.renderPlayer( screen, refresh, player, lampList, platforms, doors )

		# Check if the player has won
        counter = 0
        for lamp in lampList:
            if lamp.isLit:
                counter += 1
        if counter == len(lampList):
            win = True

        # Title label
        text = fontBig.render('Tutorial', True, white)
        textRect = text.get_rect()
        textRect.center = (400, 50)
        screen.blit(text, textRect)
        refresh.append(textRect) 
        
        # Instructions
        if page == 1:
            label("Left/Right arrow keys to move", 400, 100, white, fontSmall)
            label("Space to jump", 400, 150, white, fontSmall)
        
        	# text = fontBig.render('Tutorial', True, white)
#             textRect = text.get_rect()
#             textRect.center = (400, 50)
#             screen.blit(text, textRect)
#             refresh.append(textRect)
                
        # update the parts of the screen that need it
        pygame.display.update(refresh)

        # clear out the refresh rects
        refresh = []

        # throttle the game speed to 30fps
        gameClock.tick(30)
        
        # Handle next round
        if win == True:
            doors[1].unlock()
        
        if win != None:             
            if win == True and page < numberOfPages:
                if doors[1].win( player ):
                    pygame.mouse.set_visible(True)
                    tutorialManager(page + 1) #for more than 1 level
            elif win == True:
                if doors[1].win( player ):
                    pygame.mouse.set_visible(True)
                    levelManager()
            else:
                pygame.mouse.set_visible(True)
                levelManager()
        
        #pygame.display.update(refresh)
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
# HIGH SCORES SCREEN
##################################################
    
def highscores():

    running = True
    min_number = None
    user_array = []
    
    with open("Data/History.sdwp","r+") as f:
        for line in f:
            user_array.append(line.split(', '))
    
    user_array = sorted(user_array, key=lambda x: -int(x[2]))
    
    while running:
    
        screen.fill(black)
        
        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0))
        min_number = len(user_array)
  
        # label control 
        label('High Scores - Shadow Puppets', 400, 50, white, fontBig)
        
        if min_number == 0:
            label('No Scores, Get Playing! :)', 400, 300, white, fontBig)
        else:
            for i in range(8):
                if min_number > i:
                    factor = i + 1
                    if i > 6 and user_array[i - 7][2] == user_array[i][2]:
                        factor = i - 6
                    elif i > 5 and user_array[i - 6][2] == user_array[i][2]:
                        factor = i - 5
                    elif i > 4 and user_array[i - 5][2] == user_array[i][2]:
                        factor = i - 4
                    elif i > 3 and user_array[i - 4][2] == user_array[i][2]:
                        factor = i - 3
                    elif i > 2 and user_array[i - 3][2] == user_array[i][2]:
                        factor = i - 2
                    elif i > 1 and user_array[i - 2][2] == user_array[i][2]:
                        factor = i - 1
                    elif i > 0 and user_array[i - 1][2] == user_array[i][2]:
                        factor = i
                        
                    label('{}. {} - {}'.format(factor, user_array[i][3], user_array[i][2]), 400, 110 + i * 45, white, fontSmall)
        
        # button control
        button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
        button('Play', 400, 550, white, grey, light_grey, fontBig, do)
        button('Quit', 700, 550, white, grey, light_grey, fontBig, quit)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
                
    pygame.quit()
    quit()
    
def do():
    levelManager(True, 0, 6)
    
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
        
        # story screens
        if page == 1:
            image('cat1', 100, 100, 600, 400)
        elif page == 2:
            image('cat2', 100, 100, 600, 400)
        else:
            image('cat3', 100, 100, 600, 400)
        
        # back button
        if page == 1:
            button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
        else:
            button('Back', 100, 550, white, grey, light_grey, fontBig, story, page - 1)
        
        # skip button
        button('Skip', 700, 50, white, grey, light_grey, fontBig, tutorialManager)   
        
        # next/start button
        if page < numberOfPages:
            button('Next', 700, 550, white, grey, light_grey, fontBig, story, page + 1)
        else:
            button('Start', 700, 550, white, grey, light_grey, fontBig, tutorialManager)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if page < numberOfPages:
                    story(page + 1)
                else:
                    tutorialManager()
        
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
    
    # Sound init
    if score != None:
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
            button('Continue', 400, 400, white, grey, light_grey, fontBig, level, number, score)
        else:
            # button control
            button('Back', 100, 550, white, grey, light_grey, fontBig, startScreen)
            button('Begin', 400, 400, white, grey, light_grey, fontBig, level, number, score)
            
        button('Quit', 700, 550, white, grey, light_grey, fontBig, quit)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                level(number, score)
        
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
    
    counter = 0
    letter_read = False
    old_letter_read = False
    cycle = 0
    if score == None:
        score = 0
    max_levels = 7 # change when we add more levels
    start_time = pygame.time.get_ticks()
    pauseTime = 0 # for recording time spent reading letters
    
    rtext = fontSmall.render('', True, white) 
    
    ##################################################
    # Player init
    ##################################################

    if number == 1:
        platforms, lampList, doors, letter = layout_level4(screen)
    elif number == 2:
    	platforms, lampList, doors, letter = layout_level5(screen)
    elif number == 3:
    	platforms, lampList, doors, letter = layout_level6(screen)
    elif number == 4:
    	platforms, lampList, doors, letter = layout_level7(screen)
    elif number == 5:
    	platforms, lampList, doors, letter = layout_level8(screen)
    elif number == 6:
    	platforms, lampList, doors, letter = layout_level9(screen)
    else:
    	platforms, lampList, doors, letter = layout_level10(screen)
    
    player = Player(doors[0].center[0],doors[0].center[1], platforms)
    
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

    # set up the refresh rectangle container
    refresh = []
    screen.fill(black)

    # Draw background illuminated by lights, then render light/darkness on top
    lighting.renderLamps( screen, refresh, player, lampList, platforms, doors, letter )
    
    ##################################################
    # Enemy AI init
    ##################################################

    #spider comes in during last level
    
    spider = None
    if number == max_levels:
        spider_img = pygame.image.load("Assets/Spider.png").convert_alpha()
        spider = Enemy(screen, 300, 500, spider_img, lampList)
        frame = 0
    
    ##################################################
    # Sound init
    ##################################################

    pygame.mixer.music.stop() #stop background audio
    pygame.mixer.music.load('Audio/OPTION2.ogg')
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
    
    # Main Loop :)
    while running:
    
        # Initialize the window
        screen.fill(black)
        
        # Timer
        timer = (pygame.time.get_ticks() - start_time) - pauseTime
        current_time = 180 - (timer) / 1000.0
        
        time_min = int(current_time / 60.0)
        time_sec_int = int(current_time) % 60
        
        if current_time > 0 and time_sec_int < 10:
            text = fontSmall.render('{}:0{}'.format(time_min, time_sec_int), True, white)
            textRect = text.get_rect()
            textRect.bottomright = (790, 590)
        elif current_time > 0:
            text = fontSmall.render('{}:{}'.format(time_min, time_sec_int), True, white)
            textRect = text.get_rect()
            textRect.bottomright = (790, 590)
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
                elif event.key == pygame.K_e:
                	pauseTime += letter.display( screen, player, fontSmall, white )
            if event.type == pygame.QUIT:
                running = False
        
        player.update(spider)
        
        ##################################################
        # Enemy AI Control
        ##################################################
        
        if number == max_levels:
            frame += 1
            if not spider.isDead():
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
            lamp.checkStatus( player.rect, win )
            lamp.turnOff( spider )
            
        # Render everything to the screen
        lighting.renderLamps( screen, refresh, player, lampList, platforms, doors, letter, spider )
        lighting.renderPlayer( screen, refresh, player, lampList, platforms, doors, letter, spider )
      
        # if player touching letter, draw instructions
        
        if letter != None:
            if letter.checkCollide(player):
        	    letter.drawInstruction(screen, fontSmall, white)
            if letter.letter_closed == True:
                letter_read = True
            
        # Draw the timer after everything else
        screen.blit(text, textRect)
        refresh.append(textRect)

        # Check if the player has won
        
        counter = 0
        for lamp in lampList:
            if lamp.isLit:
                counter += 1
        if counter == len(lampList):
            if number == max_levels and player.hasKey == True:
                win = True
            elif number < max_levels:
                win = True
        
        #bonus display
        if letter_read != old_letter_read:
            old_letter_read = True
            rtext = fontSmall.render('+50', True, green)
            cycle = 0
        else:
            old_letter_read = letter_read
            if cycle == 30:
                rtext = fontSmall.render('', True, white) 
            cycle = cycle + 1
            
        rtextRect = rtext.get_rect()
        rtextRect.center = (32, 555)
        screen.blit(rtext, rtextRect)
        refresh.append(rtextRect)

        cur_score = int((1 - timer / 180000) * 1000)
        if letter_read == True:
            cur_score += 50
            
        stext = fontSmall.render('{}'.format(score + cur_score), True, white)
        stextRect = stext.get_rect()
        stextRect.bottomleft = (10, 590)
        screen.blit(stext, stextRect)
        refresh.append(stextRect)
        
        ntext = fontSmall.render('Level #{}'.format(number), True, white)
        ntextRect = ntext.get_rect()
        ntextRect.topright = (790, 10)
        screen.blit(ntext, ntextRect)
        refresh.append(ntextRect)
        
        keyStatus = ' '
        if player.hasKey:
            keyStatus = 'Key collected'
        ttext = fontSmall.render(keyStatus, True, white)
        ttextRect = ttext.get_rect()
        ttextRect.topleft = (10, 10)
        screen.blit(ttext, ttextRect)
        refresh.append(ttextRect)
        
        # update the parts of the screen that need it
        pygame.display.update(refresh)

        # clear out the refresh rects
        refresh = []

        # throttle the game speed to 30fps
        gameClock.tick(30)
        
        # Handle next round
        if win == True:
            doors[1].unlock()
        
        if win != None:             
            if win == True and number < max_levels:
                if doors[1].win(player):
                    pygame.mouse.set_visible(True)
                    score = score + cur_score # update score
                    levelManager(win, score, number) #for more than 1 level
            elif win == True:
                if doors[1].win(player):
                    pygame.mouse.set_visible(True)
                    score = score + cur_score # update score
                    endScreen(win, score, number)
            else:
                pygame.mouse.set_visible(True)
                score = score + cur_score # update score
                endScreen(win, score, number)      
        
        #pygame.display.update(refresh)
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
    pygame.mixer.music.load('Audio/BACKGROUND.ogg')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    
    text_box = pygame.Rect(400, 425, 100, 32)
    text_result = ''
    high_score = 0
    
    with open("Data/Score.sdwp","r+") as f:
        high_score = f.readline()
        if int(high_score) < score:
            f.seek(0) 
            f.truncate()
            f.write(str(score))       
      
    while running:
    
        screen.fill(black)

        bg = pygame.image.load("Assets/TransitionScreenBackground.png")
        screen.blit(bg, (0, 0))
        
        # Labels
        if win == True:
            label('You won!', 400, 200, white, fontBig)
            label('Your score was {} through level {}!'.format(score, level), 400, 275, white, fontSmall)
            
             # Enter button
            text = fontBig.render('Enter', True, white, grey)
            textRect = text.get_rect()
            textRect.center = (600, 425)
    
            mouse = pygame.mouse.get_pos()
        
            if textRect.right + 7 > mouse[0] > textRect.left - 5 and textRect.bottom + 6 > mouse[1] > textRect.top - 5:
                text = fontBig.render('Enter', True, white, light_grey)
                roundCorners(textRect, light_grey)
        
                clicked = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        clicked = True

                if clicked == True:
                    if text_result == '':
                        text_result = 'Anonymous'
                    with open("Data/History.sdwp","a+") as f:
                                f.write('{}, {}, {}, {}, {}, \n'.format(win, level, score, text_result, high_score))
                    highscores()
            else:
                text = fontBig.render('Enter', True, white, grey)
                roundCorners(textRect, grey)

            screen.blit(text, textRect)
        
            # Typing
            label('Type name:', 200, 425, white, fontSmall)
            
        else:
            label('Game Over', 400, 200, white, fontBig)
            label('You failed, try again! Your score was {} through level {}.'.format(score, level), 400, 275, white, fontSmall)
            button('Try Again', 400, 425, white, grey, light_grey, fontBig, newLevelNotifier, level, score)
            
            
        if int(high_score) < score:
            label('New High Score! Yours: {}, Previous: {}'.format(score, high_score), 400, 325, white, fontSmall)
        else:
            label('High Score: {}'.format(high_score), 400, 325, white, fontSmall)

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and win == True:
                    text_result = text_result[:-1]
                if event.key == pygame.K_RETURN and win == True:
                    if text_result == '':
                        text_result = 'Anonymous'
                    with open("Data/History.sdwp","a+") as f:
                                f.write('{}, {}, {}, {}, {}, \n'.format(win, level, score, text_result, high_score))
                    highscores()
                elif win == True:
                    text_result += event.unicode
        
        if win == True:
            # text box background
            gfxdraw.box(screen, pygame.Rect(270, 409, 260, 32), light_grey)
        
            # render text
            stext = fontSmall.render(text_result, True, white)
            if stext.get_width() > 260: # truncate if too long
                text_result = text_result[:-1]
                stext = fontSmall.render(text_result, True, white)
            stextRect = stext.get_rect()
            stextRect.center = (400, 425)
            screen.blit(stext, stextRect)
          
        pygame.display.update()
                
    pygame.quit()
    quit()
    
##################################################    
##################################################
# NOW LET'S RUN IT :)
##################################################

if __name__=="__main__":
    startScreen()
    