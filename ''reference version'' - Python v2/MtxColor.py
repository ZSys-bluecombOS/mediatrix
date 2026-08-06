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



def from_rgb_hex(code):
  if code[0] == "#":
    code = code[1:]

  return RGB([int(code[:2], 16)/255, int(code[2:4], 16)/255, int(code[4:6], 16)/255], int(code[6:8], 16)/255 if len(code) == 8 else 255)