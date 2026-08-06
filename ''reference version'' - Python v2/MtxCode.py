commands = {}
commands["add"] = lambda x, y: x + y
commands["subtract"] = lambda x, y: x - y
commands["multiply"] = lambda x, y: x * y
commands["divide"] = lambda x, y: x / y
commands["print"] = lambda x: print(x)

class Interpreter:
  def __init__(self, code):
    self.process(code)
    self.run()

  def process(self, code):
    i = 1
    formatted = []
    current_place = formatted
    before_current_place = formatted
    while i < len(code):
      if code[i] == "(":
        formatted.append([])
        before_current_place = current_place
        current_place = current_place[-1]
      elif code[i] == ")" or code[i] == " ":
        current_place = before_current_place

  def run(self):
    pass