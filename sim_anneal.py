import math
import random

def transitionProbability(cost_old, cost_new, temperature): 
  if temperature <= 0:
    return 0
  elif cost_new < cost_old:
    return 1
  else:
    return math.exp((cost_old - cost_new) / temperature)

def find_new_x(possible, f, x, best_y, temperature):
  if len(possible) == 0:
    raise ValueError("Possible points empty")
  jump = False
  for new_x in possible:
    new_y = f(new_x)
    if new_y < best_y:
      x = new_x
    elif transitionProbability(best_y, new_y, temperature) > random.random():
      jump = True
      x = new_x
  return x, jump

def seek(x,
      step,
      f,
      temperature, 
      min_x=float('-inf'),
      max_x=float('inf')):
  best_x, best_y = x, f(x)
  while temperature > -5:
    if temperature < 0: 
      step /= 2.0
    possible = [x-step, x+step, x+random.gauss(0, 1)]
    if len([i for i in possible if min_x<i<max_x]) == 0:
      continue
    x, jump = find_new_x([i for i in possible if min_x<i<max_x], f, x, best_y, temperature)
    if not jump:
      best_x = x
      best_y = f(x)

    yield x, f(x), temperature, jump
    temperature -= 0.1

if __name__ == '__main__':
  temperature = 10
  gen = seek(-1, 0.2, lambda x: x**2, temperature)
  for x, y, t, j in gen:
    print (x, y, t)

