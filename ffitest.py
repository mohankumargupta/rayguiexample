from pyray import *
from raylib import ffi


str = ffi.new("char[]", b"hello world")
print(ffi.string(str))
