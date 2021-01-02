"""
This type stub file was generated by pyright.
"""

"""This module enables interactive mode in Python Fire.

It uses IPython as an optional dependency. When IPython is installed, the
interactive flag will use IPython's REPL. When IPython is not installed, the
interactive flag will start a Python REPL with the builtin `code` module's
InteractiveConsole class.
"""
def Embed(variables, verbose=...):
  """Drops into a Python REPL with variables available as local variables.

  Args:
    variables: A dict of variables to make available. Keys are variable names.
        Values are variable values.
    verbose: Whether to include 'hidden' members, those keys starting with _.
  """
  ...

