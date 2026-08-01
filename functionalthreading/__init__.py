from functools import partial, Placeholder as _
from functionalthreading.functions import always, thunkify, chain, tap, tmap, tforeach, tfilter, reduce, tflatmap
from functionalthreading.classes import Thread

__name__ = 'functionalthreading'

__all__ = ['Thread', 'partial', '_' ,'chain', 'tap', 'tmap', 'tforeach', 'tfilter', 'reduce', 'tflatmap']
