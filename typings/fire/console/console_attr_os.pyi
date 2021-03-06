"""
This type stub file was generated by pyright.
"""

"""OS specific console_attr helper functions."""
def GetTermSize():
  """Gets the terminal x and y dimensions in characters.

  _GetTermSize*() helper functions taken from:
    http://stackoverflow.com/questions/263890/

  Returns:
    (columns, lines): A tuple containing the terminal x and y dimensions.
  """
  ...

_ANSI_CSI = '\x1b'
_CONTROL_D = '\x04'
_CONTROL_Z = '\x1a'
_WINDOWS_CSI_1 = '\x00'
_WINDOWS_CSI_2 = '\xe0'
def GetRawKeyFunction():
  """Returns a function that reads one keypress from stdin with no echo.

  Returns:
    A function that reads one keypress from stdin with no echo or a function
    that always returns None if stdin does not support it.
  """
  ...

