import math

class Equation:
  def __init__(self, equation, variables):
    pass

  def calculate(self):
    pass

class Vector_2D:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y



def linear_interpolation(a, b, t):
  return a + (b - a) * t



def dot_product_2d(a, b):
  return a.x * b.x + a.y * b.y

def cross_product_2d(a, b):
  return a.x * b.x - a.y * b.y

def distance_2d(a, b):
  dx = b.x - a.x
  dy = b.y - a.y
  return math.sqrt(dx * dx + dy * dy)

def normalize(v):
  length = math.sqrt(v.x * v.x + v.y * v.y)

  if length == 0:
    return Vector_2D(0, 0)

  return Vector_2D(v.x / length, v.y / length)

def bezier_quad(a, b, c, t):
  mt = 1 - t

  x = (
    mt*mt*a.x +
    2*mt*t*b.x +
    t*t*c.x
  )

  y = (
    mt*mt*a.y +
    2*mt*t*b.y +
    t*t*c.y
  )

  return Vector_2D(x, y)

def bezier_cubic(a, b, c, d, t):
  mt = 1 - t

  x = (
    mt**3 * a.x +
    3*mt**2*t * b.x +
    3*mt*t**2 * c.x +
    t**3 * d.x
  )

  y = (
    mt**3 * a.y +
    3*mt**2*t * b.y +
    3*mt*t**2 * c.y +
    t**3 * d.y
  )

  return Vector_2D(x, y)