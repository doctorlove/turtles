import argparse
#from copy import deepcopy
import inspect
import math

from demo import Demo
import hill_climb
import pso
import sim_anneal
import turtle

def stuck():
  turtle.setworldcoordinates(-12, -1, 12, 15)
  f = lambda x: math.fabs(x)
  demo = Demo(f)
  start = -10
  step = 20 
  demo.start(start)
  demo.bag([x for x in range(-10, 11)])
  gen = hill_climb.seek(start, step, f)
  for x, y in gen:
    demo.move(x, y, False)

def quadratic():
  turtle.setworldcoordinates(-12, -2, 12, 102)
  f = lambda x: x**2
  demo = Demo(f)
  demo.start(-10)
  demo.bag([x*0.5 for x in range(-20, 21)])
  gen = hill_climb.seek(-10, 0.5, f)
  for x, y in gen:
    demo.move(x, y, False)
  

def cosine():
  turtle.setworldcoordinates(-6.2, -12, 6.2, 12)
  f = lambda x: 10*math.cos(x)
  demo = Demo(f)
  demo.start(-6)
  demo.bag([x*0.1 for x in range(-62, 62)])
  gen = hill_climb.seek(-6, 0.1, f)
  for x, y in gen:
    demo.move(x, y, False)

def cosine_slope():
  turtle.setworldcoordinates(-6.2, -12, 6.2, 12)
  f = lambda x: -x+5*math.cos(x)
  demo = Demo(f)
  demo.start(-6)
  demo.bag([x*0.1 for x in range(-62, 62)])
  gen = hill_climb.seek(-6, 0.1, f)
  for x, y in gen:
    demo.move(x, y, False)

def bag_curve(width, height, start_x, start_y):
  x = start_x
  y = start_y
  while x < width:
    if y > 0 and x == start_x:
      y -= 0.5
    elif y == 0 and x < width:
      x += 0.5
    elif y == 0 and x >= width:
      break
    yield x, y

def slanty_bag_curve(x):
  base_x = 0.5
  width = 9.
  if x < base_x:
    y = -20.*x+10.
  elif x < width + base_x:
    y = 0
  else:
    y = 20.*x-190
  return y

def slanty_bag():
  turtle.setworldcoordinates(-2.2, -2, 12.2, 22)
  demo = Demo(slanty_bag_curve)
  demo.bag([x*0.5 for x in range(-1, 22)])

  x = -0.5
  step = 0.1
  demo.start(x)
  gen = hill_climb.seek(x, step, slanty_bag_curve)
  for x, y in gen:
    demo.move(x, y, False)


def bounds(bounded, x_points):
  if bounded:
    min_x = x_points[0]
    max_x = x_points[-1]
  else:
    min_x = float('-inf')
    max_x = float('inf')
  return min_x, max_x

def sa_demo(curr_x, step, f, temperature, x_points, min_x, max_x, *setup):
  gen = sim_anneal.seek(curr_x, step, f, temperature, min_x, max_x)
  turtle.setworldcoordinates(*setup)
  demo = Demo(f)
  demo.start(curr_x)
  demo.bag(x_points)
  for x, y, t, j in gen:
    demo.move(x, y, j)
    curr_x = x
  print (curr_x, f(curr_x))
  

def sa_cosine_turtles(bounded):
  turtle.setworldcoordinates(-6.2, -12, 6.2, 12)
  temperature = 10.0
  step = 0.2
  curr_x = [-6.0, 0, +6.0]
  f = lambda x: 10*math.cos(x)
  count = 3
  demo = [Demo(f) for _ in range(count)]
  x_points = [x*0.1 for x in range(-62, 62)]
  demo[0].bag(x_points)
  min_x, max_x = bounds(bounded, x_points)
  gens = []
  for i, x in enumerate(curr_x):
    demo[i].start(curr_x[i])
    gens.append(sim_anneal.seek(x, step, f, temperature, min_x, max_x))
  for (x1, y1, t1, j1), (x2, y2, t2, j2), (x3, y3, t3, j3) in zip(*gens):
      demo[0].move(x1, y1, j1)
      demo[1].move(x2, y2, j2)
      demo[2].move(x3, y3, j3)

def sa_quad(bounded):
  temperature = 10.0
  step = 0.2
  curr_x = -10.0
  f = lambda x: x**2
  x_points = [x*0.5 for x in range(-20, 21)]
  min_x, max_x = bounds(bounded, x_points)
  sa_demo(curr_x, step, f, temperature, x_points, min_x, max_x, -12, -2, 12, 102)


def sa_cosine(bounded):
  temperature = 12
  step = 0.2 
  curr_x = -6.0
  f = lambda x: 5*math.cos(x)
  x_points = [x*0.1 for x in range(-62, 62)]
  min_x, max_x = bounds(bounded, x_points)
  sa_demo(curr_x, step, f, temperature, 
           x_points,
           min_x, max_x, -6.2, -12, 6.2, 12)

def sa_cosine_slope(bounded):
  temperature = 12
  step = 0.2 
  curr_x = -6.0
  f = lambda x: -x+5*math.cos(x)
  x_points = [x*0.1 for x in range(-62, 62)]
  min_x, max_x = bounds(bounded, x_points)
  sa_demo(curr_x, step, f, temperature, 
           x_points,
           min_x, max_x, -6.2, -12, 6.2, 12)

def sa_slanty_bag(bounded):
  x_points = [x*0.5 for x in range(-1, 22)]
  temperature = 5.0
  curr_x = -0.5
  step = 0.1
  min_x, max_x = bounds(bounded, x_points)
  sa_demo(curr_x, step, slanty_bag_curve, temperature, 
           x_points,
           min_x, max_x, -2.2, -2, 12.2, 22)


def sa_stuck(bounded): #TODO may not get stuck - but test fails
  temperature = 12
  step = 0.1
  curr_x = -10.0
  f = lambda x: math.fabs(x)
  x_points = [x for x in range(-10, 11)]
  min_x, max_x = bounds(bounded, x_points)
  sa_demo(curr_x, step, f, temperature, 
           x_points,
           min_x, max_x, -12, -1, 12, 15)

def pso_demo(f, bounded, count, epochs, w, c1, c2): #must be bounded
  if not bounded:
    print "ERROR: failure immanent: must be bounded"
  x_points = [x*0.1 for x in range(-62, 62)]
  min_x, max_x = bounds(bounded, x_points)
  demo = [Demo(f) for _ in range(count)]
  demo[0].bag(x_points)
  gen = pso.swarm(count, min_x, max_x, epochs, f, w, c1, c2)
  start = True
  for particles in gen: 
    for i, p in enumerate(particles):
      jump = True
      if start:
        demo[i].start(p.x)
      else:
        demo[i].move(p.x, f(p.x), jump)
    start = False
      
def pso_quadratic(bounded, count, epochs, w, c1, c2): 
  turtle.setworldcoordinates(-6.2, -6, 6.2, 40)
  f = lambda x: x*x-5
  pso_demo(f, bounded, count, epochs, w, c1, c2)
      
def pso_cosine_slope(bounded, count, epochs, w, c1, c2): 
  turtle.setworldcoordinates(-6.2, -12, 6.2, 12)
  f = lambda x: -x+5*math.cos(x)
  pso_demo(f, bounded, count, epochs, w, c1, c2)

def pso_cosine(bounded, count, epochs, w, c1, c2):
  turtle.setworldcoordinates(-6.2, -12, 6.2, 12)
  f = lambda x: 5*math.cos(x)
  pso_demo(f, bounded, count, epochs, w, c1, c2)
 

if __name__ == '__main__':
  def everything(bounded, count, epochs, w, c1, c2):
    for f in fns.values():
      turtle.clearscreen()
      turtle.title(str(f))
      len_args = len(inspect.getargspec(f).args)
      if f == everything:
        continue
      elif len_args==1:
        print ("calling ", f, " with [", bounded, "]" )
        f(bounded)
      elif len_args==3:
        f(bounded, count, epochs)
      elif len_args==6:
        print args.bounded, args.count, args.epochs
        w=0.1
        c1=0.4
        c2=0.2
        f(args.bounded, args.count, args.epochs, w, c1, c2)
      else:
        print (inspect.getargspec(f).args)
        print ("calling ", f, "()") 
        f()

  fns = {'slanty_bag' : slanty_bag,
    'sa_slanty_bag' : sa_slanty_bag,
    'quadratic' : quadratic,
    'cosine' : cosine,
    'cosine_slope' : cosine_slope,
    'sa_quad' : sa_quad,
    'sa_cosine' : sa_cosine,
    'sa_cosine_slope' : sa_cosine_slope,
    'sa_cosine_turtles' : sa_cosine_turtles,
    "stuck" : stuck,
    "sa_stuck" : sa_stuck,
    "pso_quadratic": pso_quadratic, 
    "pso_cosine_slope": pso_cosine_slope,
    "pso_cosine": pso_cosine,
    "all" : everything }

  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--function", 
      choices = fns,
      help="One of " + ', '.join(fns.keys()))
  parser.add_argument("--bounded", action="store_true", help="Stops turtle leaving edges")
  parser.add_argument("--count", type=int, help="Count of particles/turtles")
  parser.add_argument("--epochs", type=int, help="How long to loop for")
  parser.add_argument("--w", type=float, help="PSO current velocity weight")
  parser.add_argument("--c1", type=float, help="PSO personal weight")
  parser.add_argument("--c2", type=float, help="PSO global weight")
  parser.set_defaults(bounded=True)
  parser.set_defaults(count=5)
  parser.set_defaults(epochs=35)
  parser.set_defaults(w=0.1)
  parser.set_defaults(c1=0.4)
  parser.set_defaults(c2=0.2)

  args = parser.parse_args()
  try:
    f = fns[args.function]
    turtle.title(args.function)
    len_args = len(inspect.getargspec(f).args)
    print len_args
    if len_args==1:
      f(args.bounded)
    elif len_args==3:
      print args.bounded, args.count, args.epochs
      f(args.bounded, args.count, args.epochs)
    elif len_args==6:
      print args.bounded, args.count, args.epochs
      w=0.1
      c1=0.4
      c2=0.2
      f(args.bounded, args.count, args.epochs, w, c1, c2)
    else:
      f()
    turtle.mainloop()
  except KeyError:
    parser.print_help()


#https://stackoverflow.com/questions/37619994/how-do-you-make-python-turtle-stop-moving
#onkey then listen
#but need some way to spot this
