#Door.py

import pygame

door_img = pygame.image.load("Assets/Door_Sprite.png")

class Door:
    def __init__(self, midbottom, exit):
        self.currentSprite = 0
        self.lastTicks = 0
#        self.image = door_img
        self.load_images()
        self.image = self.opennning[0]
        
        self.center = ( midbottom[0], midbottom[1] - (self.image.get_height()/2) )
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
        self.exit = exit
        self.entrance = not exit
        self.unlocked = False
       
    #triggers next level load
    def get_images(self, a, b, wid, hei):
        sprite = pygame.image.load('Assets/Door_Sprite.png').convert()
        getimage = pygame.Surface((wid,hei))
        getimage.blit(sprite,(0,0),(a,b,wid,hei))
        getimage = pygame.transform.scale(getimage,(wid//6, hei//6))
        return getimage

    def load_images(self):
        self.opennning = [self.get_images(20,20,413,333),self.get_images(20,373,408,326),self.get_images(453,369,410,327),self.get_images(453,20,410,329)]
        for pic in self.opennning:
            pic.set_colorkey((0,0,0))

    #triggers next level load
    def win(self, player):
        if(self.exit and player.rect.collidepoint( self.center ) and self.unlocked):
            return True
    
    #unlocks the door
    def unlock(self):
        if not self.unlocked:
            self.unlocked = True
            #open door animation/sound
            pygame.mixer.music.load('Audio/Door.aif')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
        
        self.doorMotion()
        
    def doorMotion(self):
        nowTicks = pygame.time.get_ticks()
        if self.currentSprite < 3:
            if nowTicks - self.lastTicks > 300:
                self.lastTicks = nowTicks
                self.currentSprite = self.currentSprite + 1
                #bottom = self.rect.bottom
                self.image = self.opennning[self.currentSprite]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom