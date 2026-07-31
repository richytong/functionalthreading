from typing import overload
import threading

def _chain(argument, funcs):
    ret = argument
    for func in funcs:
        ret = func(ret)
    return ret

@overload
def chain(*funcs):
    '''
Returns a function of chained functions that expects the arguments to the first function. Each function in the chain is evaluated in series starting from the first function, passing the return value as the first and only argument to the next function. The return value of the chain is the return value of the last function.

```python
my_function_chain = chain(
    lambda m, n: m + n + 1,
    lambda n: n ** 2,
    lambda n: n / 3,
    print
)

my_function_chain(2, 3)
```
    '''
    inner_funcs = (argument,) + funcs
    def inner_func(inner_argument):
        return _chain(inner_argument, inner_funcs)
    return inner_func

def chain(argument, *funcs):
    '''
Chains functions together. Each function is evaluated in series starting from the first function, passing the return value as the first and only argument to the next function. The return value of the chain is the return value of the last function.

```python
chain(
    2,
    lambda n: n + 1,
    lambda n: n ** 2,
    lambda n: n / 3,
    print
)
```
    '''
    if callable(argument):
        inner_funcs = (argument,) + funcs
        def inner_func(inner_argument):
            return _chain(inner_argument, inner_funcs)
        return inner_func
    return _chain(argument, funcs)

def tap(func):
    '''
Calls a function with an argument, returning the argument.

```python
chain(
    1,
    lambda n: n + 1,
    tap(print),
    lambda n: n + 2,
    tap(print),
    lambda n: n + 3,
    print
)
```
    '''
    def inner_func(argument):
        func(argument)
        return argument
    return inner_func

__all__ = ['chain', 'tap']
