from functools import partial, Placeholder as _
from package import version
from functions import chain, tap, tmap

__version__ = version

__name__ = 'functionalthreading'

__all__ = ['partial', '_' ,'chain', 'tap', 'tmap']
