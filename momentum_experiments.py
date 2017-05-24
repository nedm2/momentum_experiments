import pygame, sys, os
from pygame.locals import *
import math
from random import random

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

class Vector:
  def __init__(self, x=0, y=0):
    self.x = float(x)
    self.y = float(y)

  def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y)

  def __mul__(self, scale):
    return Vector(scale*self.x, scale*self.y)

  def __rmul__(self, scale):
    return self*scale

  def int_x(self):
    return toint(self.x)

  def int_y(self):
    return toint(self.y)

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def magnitude(self):
    return math.sqrt(self.x**2 + self.y**2)

  def unit_vector(self):
    if abs(self.x) < tinyFloat and abs(self.y) < tinyFloat:
      return Vector(0,0)
    else:
      return Vector(self.x/self.magnitude(), self.y/self.magnitude())

  def angle_rad(self):
    return math.atan2(self.y, self.x)

  def getComponent(self, theta):
    alpha = self.angle_rad() - theta
    magnitude = math.cos(alpha)*self.magnitude()
    return Vector(math.cos(theta)*magnitude, math.sin(theta)*magnitude)

  def getNormalComponent(self, theta):
    alpha = self.angle_rad() - theta
    magnitude = math.sin(alpha)*self.magnitude()
    return Vector(math.cos(theta + (math.pi/2))*magnitude, math.sin(theta + (math.pi/2))*magnitude)

  def __str__(self):
    return "Vector (%.3f, %.3f)" % (self.x, self.y)

  def distance(self, v):
    return math.sqrt((self.x - v.x)**2 + (self.y - v.y)**2)
    
  def __repr__(self):
    return self.__str__()

class Ball():
  def __init__(self, position=Vector(900.0,450.0), velocity=Vector(-0.97,-0.5)):
    self.diameter = 51.0
    self.radius = self.diameter/2
    self.radius = 35.0
    self.position = position
    self.velocity = velocity
    self.color = (150, 0,0) 

  def update(self):
    self.position += self.velocity

  def draw(self, screen):
    pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))

class Simulation():
    def __init__(self):
        self.b1 = Ball(Vector(50.0, 250.0), Vector(1.0, 0.0))
        self.b2 = Ball(Vector(950.0, 250.0), Vector(-1.0, 0.0))
        self.cushions = 0

    def update(self):
        self.b1.update()
        self.b2.update()
        if self.b1.position.distance(self.b2.position) < (self.b1.radius + self.b2.radius):
            self.b1.velocity = Vector(0,0)
            self.b2.velocity = Vector(0,0)


    def draw(self, screen):
        self.b1.draw(screen)
        self.b2.draw(screen)

def input(events): 
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

simulation = Simulation()
simulationRunning = True

while True: 
  screen.fill((0,0,0))
  simulation.update()
  simulation.draw(screen)
  pygame.display.flip()
  input(pygame.event.get())
  clock.tick(300)
