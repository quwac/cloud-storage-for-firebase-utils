"""
This type stub file was generated by pyright.
"""

import functools

"""This module has components that use Python 3 specific syntax."""
def identity(arg1, arg2: int, arg3=..., arg4: int = ..., *arg5, arg6, arg7: int, arg8=..., arg9: int = ..., **arg10):
  ...

class KeywordOnly(object):
  def double(self, *, count):
    ...
  
  def triple(self, *, count):
    ...
  
  def with_default(self, *, x=...):
    ...
  


class LruCacheDecoratedMethod(object):
  @functools.lru_cache()
  def lru_cache_in_class(self, arg1):
    ...
  


@functools.lru_cache()
def lru_cache_decorated(arg1):
  ...

