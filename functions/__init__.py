from threading import Thread
import itertools

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
        inner_funcs = (argument,) + funcs
        def inner_func(inner_argument):
            return _chain(inner_argument, inner_funcs)
        return inner_func
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

class _Thread(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.value = None
        self.target = kwargs['target']
        self.args = kwargs['args']

    def run(self):
        self.value = self.target(*self.args)

def tmap(array_or_tuple, func):
    """Map a function concurrently across each element of an array or tuple.

    Each function invokation happens in a separate thread.

    ```python
    squared = tmap([1, 2, 3], lambda n: n ** 2)
    ```

    """
    length = len(array_or_tuple)
    threads = []
    index = 0
    args = [array_or_tuple]
    while index < length:
        t = _Thread(target=func, args=[array_or_tuple[index]])
        t.start()
        threads.append(t)
        index += 1
    index = 0
    result = []
    while index < length:
        t = threads[index]
        t.join()
        result.append(t.value)
        index += 1
    if isinstance(array_or_tuple, tuple):
        return tuple(result)
    return result

__all__ = ['chain', 'tap', 'tmap']
