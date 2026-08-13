# This will be limited in its ability to open files for a long time.

# I may make pages for https://wiki.bluecomb.dpdns.org/wiki/Misc/File_types as I make parsers,
# just so that they're documented at the same time I'm learning them

class ParsedFile:
  def __init__(self, file: str | bytes | bytearray):
    if type(file) == str:
      with open(file, "rb") as openFile:
        self.orig_content = openFile.read()
    else:
      self.orig_content = file

    pass