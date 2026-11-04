class ParsedFile:
  def __init__(self, file: str | bytes | bytearray):
    if type(file) == str:
      with open(file, "rb") as openFile:
        self.orig_content = openFile.read()
    else:
      self.orig_content = file

    pass