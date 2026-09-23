class MtxVector:
  class Path:
    def __init__(self):
      self.points = []

  def __init__(self, size):
    self.width = size[0]
    self.height = size[1]
    self.paths = []

  def render(self):
    pass