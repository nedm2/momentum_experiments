import pygame, sys, os
from pygame.locals import *
import math
from random import random
from Vector import Vector

#params
win_width = 1000.0
win_height = 500.0
border = 0.1 
border_width = border*win_width
border_height = border*win_height
updatesPerFrame = 20

#globals
restartSimulation = True

def toint(i): return int(round(i))

########### Simulation ##############


class Ball():
    def __init__(self, position=Vector(900.0,450.0), velocity=Vector(-0.97,-0.5), m=100):
      self.diameter = 51.0
      self.radius = self.diameter/2
      self.radius = 35.0
      self.position = position
      self.velocity = velocity
      self.color = (150, 0,0) 
      self.mass = m

    def update(self):
      self.position += self.velocity

    def draw(self, screen):
      pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))

    def inViewAndMoving(self):
        return self.position.x >= 0 \
           and self.position.x <= win_width \
           and self.position.y >= 0 \
           and self.position.y <= win_height \
           and self.velocity.magnitude() > 0.3

class Simulation():
    def __init__(self, b1=Vector(50.0, 250.0), b1v=Vector(1.0, 0.0), b2=Vector(500.0, 250.0), b2v=Vector(0.0, 0.0), b1m=1, b2m=1):
        self.b1 = Ball(b1, b1v, b1m)
        self.b2 = Ball(b2, b2v, b2m)
        self.cushions = 0

    def momentum(self):
        #Calculate the vector of force from b2 to b1
        print(self.b1.position, self.b2.position)
        impVelComp1 = self.b1.velocity.component(self.b2.position - self.b1.position)
        impVelComp2 = self.b2.velocity.component(self.b1.position - self.b2.position)
        velInit1 = impVelComp1.magnitude()
        velInit2 = impVelComp2.magnitude()

        # Take b1 direction as positive, must negate magnitudes in opposite direction
        if self.b1.velocity.alpha(self.b2.velocity) > math.pi/2:
            velInit2 *= -1
            impVelComp2 *= -1

        velFin1 = velInit1*((self.b1.mass - self.b2.mass) / (self.b1.mass + self.b2.mass)) + velInit2*((2*self.b2.mass)/(self.b1.mass+self.b2.mass))
        velFin2 = velInit2*((self.b2.mass - self.b1.mass) / (self.b2.mass + self.b1.mass)) + velInit1*((2*self.b1.mass)/(self.b2.mass+self.b1.mass))

        print(velFin2)

        if abs(velInit1) < 0.01:
            impVelComp1 = impVelComp2
        if abs(velInit2) < 0.01:
            impVelComp2 = impVelComp1

        self.b1.velocity = self.b1.velocity.component(impVelComp1.rotated(math.pi/2)) + velFin1*((impVelComp1).unit_vector())
        self.b2.velocity = self.b2.velocity.component(impVelComp2.rotated(math.pi/2)) + velFin2*((impVelComp2).unit_vector())


    def update(self):
        self.b1.update()
        self.b2.update()
        if self.b1.position.distance(self.b2.position) < (self.b1.radius + self.b2.radius):
            self.momentum()


    def draw(self, screen):
        self.b1.draw(screen)
        self.b2.draw(screen)

    def objectsInViewAndMoving(self):
        return self.b1.inViewAndMoving() or self.b2.inViewAndMoving()

def events(events): 
  for event in events: 
      if event.type == QUIT: 
          sys.exit(0) 


################# main ################

pygame.init()
window = pygame.display.set_mode((toint(win_width), toint(win_height)))
pygame.display.set_caption('Momentum experiments')
screen = pygame.display.get_surface() 
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

for i in range(20):

    simulation = Simulation(b2=Vector(950.0, 200 + i*5), b2v=Vector(-1.0, 0), b1v=Vector(0,0), b1=Vector(500, 250), b2m=2.0)

    while simulation.objectsInViewAndMoving(): 
      screen.fill((0,0,0))
      simulation.update()
      simulation.draw(screen)
      pygame.display.flip()
      events(pygame.event.get())
      clock.tick(300)
