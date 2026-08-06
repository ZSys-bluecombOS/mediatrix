class MtxColor_base:
  def __init__(self, colors, alpha: float, color_size, color_type):
    if len(colors) != color_size:
      raise Exception(f"Wrong number of color parts for {color_type}")
    else:
      self.color = colors

    self.alpha = alpha

class RGB(MtxColor_base):
  def __init__(self, colors, alpha):
    super().__init__(colors, alpha, 3)