class VImage:
  class Path:
    def __init__(self, points, color):
      self.points = points
      self.color = color

  def __init__(self, size):
    self.width = size[0]
    self.height = size[1]
    self.paths = []

  def render(self):
    pass