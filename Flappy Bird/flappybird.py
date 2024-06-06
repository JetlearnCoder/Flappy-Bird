import pygame 
from pygame.locals import *
import random


pygame.init()
clock = pygame.time.Clock()
fps = 60

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Flappy Bird')
groundscroll = 0
scrollspeed = 4
fly = False
game_over = False
pipegap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency


bg = pygame.image.load("background.png")
groundimage = pygame.image.load("ground.png")
run = True

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'flappy{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0 
        self.clicked = False
    
    def update(self):
        if fly == True:
            self.vel = self.vel + 0.5
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
            if self.vel > 8:
                self.vel = 8
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            #6-fly for only one click and reset the click again
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= 3:
                self.index = 0
        self.image = self.images[self.index]

        
        
bird_group = pygame.sprite.Group()
flappy = Bird(100,450)
bird_group.add(flappy)

            
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipegap/2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipegap/2)]
        
    def update(self):
        self.rect.x -= scrollspeed
        if self.rect.right < 0:
            self.kill()


pipe_group = pygame.sprite.Group()


        
while run:
    clock.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(groundimage,(groundscroll,768))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    if game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(800,int(800/2)+ pipe_height, -1)
            top_pipe = Pipe(800,int(800/2)+ pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        groundscroll -= scrollspeed
        if abs(groundscroll) > 35:
            groundscroll = 0
        pipe_group.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and game_over == False:
            fly = True
    if flappy.rect.bottom > 768:
        game_over = True
        fly = False
    pygame.display.update()
    
    
    
    
    
    


