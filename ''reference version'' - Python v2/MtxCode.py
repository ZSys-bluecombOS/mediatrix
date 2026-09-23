class Interpreter:
  def __init__(self, code):
    self.process(code)
    self.run()
    self.commands = {}

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

  def run(self, vars=None):
    pass