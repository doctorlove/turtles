import turtle
import random

def dragon():
#https://trinket.io/python/c06f77c8e6
#   Dragon curve using L-system
#   Authour:Alan Richmond, Python3.codes
#   https://en.wikipedia.org/wiki/L-system

  def X(n):
    if n>0:  L("X+YF+",n)
  def Y(n):
    if n>0:  L("-FX-Y",n)
      
  def L(s,n):
    for c in s:
      if   c=='-': turtle.lt(90)
      elif c=='+': turtle.rt(90)
      elif c=='X': X(n-1)
      elif c=='Y': Y(n-1)
      elif c=='F': turtle.fd(12)
      print turtle.position()
        
  turtle.bgcolor('black')
  turtle.pencolor('red')
  turtle.up()
  turtle.goto(-20, 160)
  turtle.down()
  X(10)
  turtle.hideturtle()

  turtle.mainloop()  


if __name__ == '__main__':
  dragon()

