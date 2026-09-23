class MtxImage:
  def __init__(self, size, color):
    self.width = size[0]
    self.height = size[1]
    self.image = [[color for y in size[0]] for x in size[1]]