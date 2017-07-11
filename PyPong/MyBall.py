import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([640,480])
score = 0
score_font = pygame.font.Font(None, 50)
score_surf = score_font.render(str(score), 1, (0, 0, 0))

class MyBallClass(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
       
        
    def move(self):
        global score, score_font, score_surf
        self.rect = self.rect.move(self.speed)
        hit_wall = pygame.mixer.Sound("./sound_resource/hit_wall.wav")
        get_point = pygame.mixer.Sound("./sound_resource/get_point.wav")
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(score), 1, (0, 0, 0))
        if self.rect.left < 0 or self.rect.right >= screen.get_width():
            self.speed[0] = - self.speed[0]
            hit_wall.play()

        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
            score = score + 1
            score_surf = score_font.render(str(score), 1, (0, 0, 0))
            get_point.play()
            
    
