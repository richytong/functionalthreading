from functools import partial, Placeholder as _
from functionalthreading.classes import Thread

def always(argument):
    """Always return a value.

    ```python
    always5 = always(5)

    always5()
    ```

    """
    def inner_func():
        return argument
    return inner_func

def thunkify(func, *args, **kwargs):
    """Create a thunk from a function and arguments.

    A thunk is a function that takes no arguments and executes the provided function with the provided arguments each call.

    ```python
    printHello = thunkify(print, 'Hello')

    printHello()
    printHello()
    printHello()
    ```

    """
    def inner_func():
        return func(*args, **kwargs)
    return inner_func

def _chain(argument, funcs):
    ret = argument
    for func in funcs:
        ret = func(ret)
    return ret

def chain(argument, *funcs):
    """Chain functions together.

    Each function is evaluated in series starting from the first function, passing the return value as the first and only argument to the next function. The return value of the chain is the return value of the last function.

    ```python
    chain(
        2,
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n / 3,
        print
    )
    ```

    If the first non-function argument is omitted, returns a function of chained functions that expects the non-function argument.

    ```python
    my_function_chain = chain(
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n / 3,
        print
    )

    my_function_chain(2)
    ```

    """
    if callable(argument):
        return partial(_chain, _, (argument,) + funcs)
    return _chain(argument, funcs)

def tap(func):
    """Call a function with an argument, returning the argument.

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

    """
    def inner_func(argument):
        func(argument)
        return argument
    return inner_func

def _tmap(argument, func):
    length = len(argument)
    threads = []
    index = 0
    args = [argument]
    while index < length:
        t = Thread(target=func, args=[argument[index]])
        t.start()
        threads.append(t)
        index += 1
    result = []
    for t in threads:
        t.join()
        result.append(t.result)
    if isinstance(argument, tuple):
        return tuple(result)
    return result

def tmap(*args):
    """Map a function concurrently across each element of an array or tuple.

    Each function invokation happens in a separate thread.

    ```python
    squared = tmap([1, 2, 3], lambda n: n ** 2)
    ```

    If the array or tuple argument is omitted, returns a function of the mapping function that expects the argument.

    ```python
    my_mapping_func = tmap(lambda n: n ** 2)
    squared = my_mapping_func([1, 2, 3])
    ```

    """
    if callable(args[0]):
        return partial(_tmap, _, args[0])
    return _tmap(*args)

def _tforeach(argument, func):
    length = len(argument)
    threads = []
    index = 0
    args = [argument]
    while index < length:
        t = Thread(target=func, args=[argument[index]])
        t.start()
        threads.append(t)
        index += 1
    for t in threads:
        t.join()
    return None

def tforeach(*args):
    """Execute a function concurrently for each element of an array or tuple.

    Each function invokation happens in a separate thread.

    ```python
    tforeach([1, 2, 3], print)
    ```

    If the array or tuple argument is omitted, returns a function of the function to execute that expects the argument.

    ```python
    my_foreach_func = tforeach(print)
    my_foreach_func([1, 2, 3])
    ```

    """
    if callable(args[0]):
        return partial(_tforeach, _, args[0])
    return _tforeach(*args)

__name__ = 'functions'

__all__ = ['always', 'thunkify', 'chain', 'tap', 'tmap', 'tforeach']
