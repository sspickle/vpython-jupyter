# importlib.metadata is stdlib (3.8+); pkg_resources is a setuptools import that
# is deprecated upstream and, more practically, is simply absent in some
# environments — Pyodide/wasm among them, where importing vpython failed at this
# very first line with ModuleNotFoundError: No module named 'pkg_resources'.
from importlib.metadata import version as _distribution_version, PackageNotFoundError

from .gs_version import glowscript_version

try:
    __version__ = _distribution_version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass
__gs_version__ = glowscript_version()

del glowscript_version
del _distribution_version
del PackageNotFoundError

# Keep the remaining imports later to  ensure that __version__ and
#  __gs_version__ exist before importing vpython, which itself imports
# both of those.

from ._notebook_helpers import __is_spyder

from .vpython import canvas

import sys as _sys
if _sys.platform == 'emscripten':
    # Boot the wasm transport EAGERLY: its patches must land before the
    # star-imports below bind rate/sleep into the package namespace.
    from . import trinket_worker as _tw
del _sys

# Need to initialize canvas before user does anything and before
scene = canvas()

from .vpython import *
from .shapespaths import *
from ._vector_import_helper import *
from .rate_control import rate

# vpython is showing up in the
# namespace, so delete them
del vpython

# cyvector may be in the namespace. Get rid of it
try:
    del cyvector
except NameError:
    pass

# import for backwards compatibility
from math import *
from numpy import arange
from random import random

if __is_spyder():
    from ._notebook_helpers import _warn_if_spyder_settings_wrong
    _warn_if_spyder_settings_wrong()
