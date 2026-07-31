class MtxImage:
  def __init__(self, size, color):
    self.image = [[color for y in size[0]] for x in size[1]]