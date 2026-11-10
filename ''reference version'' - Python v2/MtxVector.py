from PIL import Image
from MtxMath import bezier_quad, bezier_cubic, Vector_2D

class Line:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def side_of(self, point):
    return (
      (self.end.x - self.start.x)
      * (point.y - self.start.y)
      -
      (self.end.y - self.start.y)
      * (point.x - self.start.x)
    )

  def is_right_of(self, point):
    return self.side_of(point) < 0



class BezierQuad:
  def __init__(self, start, end, curve):
    self.start = start
    self.end = end
    self.curve = curve

  def to_lines(self, samples):
    curve_points = []
    for i in range(samples):
      curve_points.append(bezier_quad(self.start, self.curve, self.end, i/samples))

    return [Line(curve_points[x], curve_points[x+1]) for x in range(len(curve_points)-1)]

  def is_right_of(self, point):
    lines = self.to_lines(32)
    return sum([x.is_right_of(point) for x in lines]) > 0



class BezierCubic:
  def __init__(self, start, end, curve1, curve2):
    self.start = start
    self.end = end
    self.curve1 = curve1
    self.curve2 = curve2

  def to_lines(self, samples):
    curve_points = []
    for i in range(samples):
      curve_points.append(bezier_cubic(self.start, self.curve1, self.curve2, self.end, i/samples))

    return [Line(curve_points[x], curve_points[x+1]) for x in range(len(curve_points)-1)]

  def is_right_of(self, point):
    lines = self.to_lines(32)
    return sum([x.is_right_of(point) for x in lines]) > 0



class Path:
  def __init__(self, segments, fill):
    self.segments = segments
    self.fill = fill



class VImage:
  def __init__(self, size):
    self.width = size[0]
    self.height = size[1]
    self.paths = []

  def render(self):
    thing = Image.new("RGB", (self.width, self.height), (0, 0, 0))
    imgload = thing.load()
    for i in range(self.height):
      for j in range(self.width):
        imgload[j, i] = self.paths[0]



if __name__ == "__main__":
  thing = VImage([100, 100])
  thing.paths.append(
    Path(
      [
        Line(Vector_2D(20, 20), Vector_2D(20, 40)),
        Line(Vector_2D(20, 40), Vector_2D(40, 40)),
        Line(Vector_2D(40, 40), Vector_2D(20, 20))
      ]
    )
  )
  thing.render()