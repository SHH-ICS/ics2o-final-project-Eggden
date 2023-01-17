import os
import sys
import math
import random
import pygame

WIDTH = 670
HEIGHT = 154

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('ICS2O - RST 2022-2023')

class Dino:
  
  def __init__(self):
    self.width = 44
    self.height = 44
    self.x = 50
    self.y = 95
    self.texture_num = 0
    self.dy = 3.5
    self.gravity = 1.2
    self.onground = True
    self.jumping = False
    self.jump_stop = 10
    self.falling = False
    self.fall_stop = self.y
    self.set_texture()
    self.set_sound()
    self.show()

  def update(self, loops):
    #Jump
    if self.jumping:
      self.y -= self.dy
      if self.y <= self.jump_stop:
        self.fall()
      
    #Fall
    elif self.falling:
      self.y += self.gravity * self.dy
      if self.y >= self.fall_stop:
        self.stop()
      
    #movement
    elif self.onground and loops % 4 == 0:
        self.texture_num = (self.texture_num + 2) % 3
        self.set_texture()

  def show(self):
    screen.blit(self.texture, (self.x, self.y))

  def set_texture(self):
    path = os.path.join(f'assets/images/dino{self.texture_num}.png')
    self.texture = pygame.image.load(path)
    self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

  def set_sound(self):
    path = os.path.join('assets/Sounds/Jump.wav')
    self.sound = pygame.mixer.Sound(path)

  def jump(self):
    self.sound.play()
    self.jumping = True
    self.onground = False

  def fall(self):
    self.jumping = False
    self.falling = True

  def stop(self):
    self.falling = False
    self.onground = True

class BG:
  
  def __init__(self, x):
    self.width = WIDTH
    self.height = HEIGHT
    self.x = x
    self.y = 0
    self.self_texture()
    self.show()

  def update(self, dx):
    self.x += dx
    if self.x <= -WIDTH:
      self.x = WIDTH
  
  def show(self):
    screen.blit(self.texture, (self.x, self.y))
    
  def self_texture(self):
    path = os.path.join('assets/images/bg.jpg')
    self.texture = pygame.image.load(path)
    self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
                                        
class Cactus:

  def __init__(self, x):
    self.width = 36
    self.height = 60
    self.x = x
    self.y = 80
    self.set_texture()
    self.show()
    

  def update(self, dx):
    self.x += dx

  def show(self):
    screen.blit(self.texture, (self.x, self.y))

  def set_texture(self):
    path = os.path.join('assets/images/Something.png')
    self.texture = pygame.image.load(path)
    self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collsion:

  def between(self, obj1, obj2):
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < 25

class Score:

  def __init__(self, hs):
    self.hs = hs
    self.act = 0
    self.font = pygame.font.SysFont('Impact', 30)
    self.color = (0,0,0)
    self.set_sound()
    self.show()

  def update(self, loops):
    self.act = loops//10
    self.check_hs()
    self.check_sound()

  def show(self):
    self.lbl = self.font.render(f' {self.act}  {self.hs}', 0.1, self.color)
    lbl_width = self.lbl.get_rect().width
    screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

  def set_sound(self):
    path = os.path.join('assets/Sounds/point.wav')
    self.sound = pygame.mixer.Sound(path)

  def check_hs(self):
    if self.act >= self.hs:
      self.hs = self.act

  def check_sound(self):
    if self.act % 100 == 0 and self.act != 0:
      self.sound.play()
    
class Game:
  
  def __init__(self, hs=0):
    self.bg = [BG(x=0), BG(x=WIDTH)]
    self.dino = Dino()
    self.obstacles = []
    self.collsion = Collsion()
    self.score = Score(hs)
    self.speed = 3
    self.playing = False
    self.set_sound()
    self.set_labels()
  
  def set_labels(self):
    bigfont = pygame.font.SysFont('Impact', 40, bold = True)
    smallfont = pygame.font.SysFont('Impact', 17, bold = True)
    self.biglbl = bigfont.render(f'YOU HIT A CACTUS', 5, (255, 20, 0))
    self.smalllbl = smallfont.render(f'PRESS R TO RESPAWN', 1, (0, 0, 0))

  def set_sound(self):
    path = os.path.join('assets/Sounds/death.wav')
    self.sound = pygame.mixer.Sound(path)
    
  def start(self):
    self.playing = True

  def over(self):
    self.sound.play()
    screen.blit(self.biglbl, (WIDTH // 2 - self.biglbl.get_width() // 2, HEIGHT // 4))
    screen.blit(self.smalllbl, (WIDTH // 2 - self.smalllbl.get_width() // 2, HEIGHT // 2))
    self.playing = False

  def tospawn(self, loops):
    return loops % 100 == 0

  def spawn_cactus(self):
    #list for cactus
    if len(self.obstacles) > 0:
     prev_cactus = self.obstacles[-1]
     x = random.randint(prev_cactus.x + self.dino.width + 84, WIDTH + prev_cactus.x +self.dino.width + 84)
      
     #empty list
    else:
        x = random.randint(WIDTH + 100, 1000)

    #create cactus
    cactus = Cactus(x)
    self.obstacles.append(cactus)

  def restart(self):
    self.__init__(hs=self.score.hs)

def main():

  #objects
  game = Game()
  dino = game.dino

  #variables
  clock = pygame.time.Clock()
  loops = 0
  
  #mainloop 
  while True:

   if game.playing:

     loops += 1
    
     # Background
     for bg in game.bg:
       bg.update(-game.speed)
       bg.show()

     #dino
     dino.update(loops)
     dino.show() 

     #Cactus

     if game.tospawn(loops):
      game.spawn_cactus()

     for cactus in game.obstacles:
      cactus.update(-game.speed)
      cactus.show()

      #Collsion
      if game.collsion.between(dino, cactus):
        game.over()

      #Score
      game.score.update(loops)
      game.score.show()

   #events
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
     pygame.quit
     sys.exit

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
         if dino.onground:
           dino.jump()

         if not game.playing:
          game.start()


        if event.key == pygame.K_r:
          game.restart()
          dino = game.dino
          loops = 0
       
   clock.tick(80)
   pygame.display.update()

main()