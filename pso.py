#See https://visualstudiomagazine.com/Articles/2013/11/01/Particle-Swarm-Optimization.aspx?Page=2

import math
import random

class Particle:
  def __init__(self, x, name):
    self.x = x
    self.best = x
    self.velocity = random.random() #TODO try 0 instead
    self.name = name
    self.history = []

  def __str__(self):
    return self.name + "::" + 'x:' + str(self.x) + ', best:' + str(self.best) + ', velocity:' + str(self.velocity)

def move(particles, min_x, max_x, f):
  for particle in particles:
    x = particle.x + particle.velocity 
    if max_x < x:
      particle.x = max_x
    elif min_x > x:
      particle.x = min_x
    else:
      particle.x = x
    particle.history.append((particle.x, particle.velocity))
    if f(particle.x) < f(particle.best):
      particle.best = particle.x

def update_velocity(particles, best, w=0.1, c1=0.4, c2=0.2):
  for particle in particles:
    #r1 = 1.
    #r2 = 1.
    r1 = random.random(); 
    r2 = random.random(); 
    particle.velocity = w * particle.velocity + c1 * r1 * (particle.best - particle.x) + c2 * r2 * (best - particle.x)
    if -0.00001 < particle.velocity < 0.00001:
      print particle.name, "slowing down near", particle.x
      #raise Exception("velocity", particle.velocity)

def find_best(particles, best, f):
  for particle in particles:
    if f(particle.x) < f(best):
      best = particle.x
  return best

def initialise(count, min_x, max_x):
  particles = []
  for i in range(count):
    x = random.uniform(min_x, max_x)
    particles.append(Particle(x, str(i)))
  return particles


def swarm(count, min_x, max_x, epochs, f, w=0.1, c1=0.4, c2=0.2):
  print "w", w, "c1", c1, "c2", c2
  particles = initialise(count, min_x, max_x)
  best = find_best(particles, particles[0].best, f)

  for _ in range(epochs):
    yield particles
    best = find_best(particles, best, f)
    update_velocity(particles, best, w, c1, c2)
    move(particles, min_x, max_x, f)

  print "best", best


if __name__ == '__main__':
  f = lambda x: -x+5*math.cos(x)
  x_points = [x*0.1 for x in range(-62, 62)]
  count = 10
  min_x = 0
  max_x = 4
  epochs = 100
  gen = swarm(count, min_x, max_x, epochs, f)
  for particles in gen:
    for p in particles:
      print p
    #curr_x = particles
  #print "curr_x", str(curr_x) 
  print "Final"
  for p in particles:
    print p, f(p.x)


	
