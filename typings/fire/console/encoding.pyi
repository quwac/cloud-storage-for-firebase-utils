"""
This type stub file was generated by pyright.
"""

"""A module for dealing with unknown string and environment encodings."""
def Encode(string, encoding=...):
  """Encode the text string to a byte string.

  Args:
    string: str, The text string to encode.
    encoding: The suggested encoding if known.

  Returns:
    str, The binary string.
  """
  ...

def Decode(data, encoding=...):
  """Returns string with non-ascii characters decoded to UNICODE.

  UTF-8, the suggested encoding, and the usual suspects will be attempted in
  order.

  Args:
    data: A string or object that has str() and unicode() methods that may
      contain an encoding incompatible with the standard output encoding.
    encoding: The suggested encoding if known.

  Returns:
    A text string representing the decoded byte string.
  """
  ...

def GetEncodedValue(env, name, default=...):
  """Returns the decoded value of the env var name.

  Args:
    env: {str: str}, The env dict.
    name: str, The env var name.
    default: The value to return if name is not in env.

  Returns:
    The decoded value of the env var name.
  """
  ...

def SetEncodedValue(env, name, value, encoding=...):
  """Sets the value of name in env to an encoded value.

  Args:
    env: {str: str}, The env dict.
    name: str, The env var name.
    value: str or unicode, The value for name. If None then name is removed from
      env.
    encoding: str, The encoding to use or None to try to infer it.
  """
  ...

def EncodeEnv(env, encoding=...):
  """Encodes all the key value pairs in env in preparation for subprocess.

  Args:
    env: {str: str}, The environment you are going to pass to subprocess.
    encoding: str, The encoding to use or None to use the default.

  Returns:
    {bytes: bytes}, The environment to pass to subprocess.
  """
  ...

