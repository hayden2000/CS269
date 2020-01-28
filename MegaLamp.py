import sys
import pygame
img = pygame.image.load("Assets/bosslamp.png").convert()
vec = pygame.math.Vector2

class MegaLamp:
    
    def __init__(self, x_pos, y_pos, platforms, width = 30, height = 50):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.bottom = y_pos
        self.moveRight = True
        self.vel = vec(3,0)
        self.platforms = platforms

    def hitX(self):
        for platform in self.platforms:            
            if self.rect.colliderect(platform.collisionRect):
                #left
                if self.vel.x > 0:
                    self.vel.x = -1* self.vel.x
                    self.moveRight = False
                #right
                elif self.vel.x < 0:
                    self.vel.x = -1*self.vel.x
                    self.moveRight = True
    
    def hitY(self):
        for platform in self.platforms:
            if self.rect.colliderect(platform.collisionRect):
                #top
                if self.vel.y < 0:
                    self.rect.bottom = platform.collisionRect.bottom + 30
                    self.vel.y = 0
    
    def update(self):
        print(self.rect)
        self.vel.y = - 1
        if self.rect.bottom > 595:
            self.rect.bottom = 0
        if self.rect.x > 795:
            self.vel.x = -1*self.vel.x
            self.moveRight = False
        if self.rect.x < 5:
            self.vel.x = -1*self.vel.x
            self.moveRight = True
        self.rect.x += self.vel.x
        
        #self.hitX()

        self.rect.y += self.vel.y

        self.hitY()