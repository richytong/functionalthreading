from functools import partial, Placeholder as _, reduce as _reduce
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
    """Map a function concurrently across each element of a list or tuple.

    A mapper is a function that specifies a single element of a list or tuple and returns a corresponding element of the resulting list or tuple. Each mapper invocation happens in a separate thread.

    ```python
    squared = tmap([1, 2, 3], lambda n: n ** 2)
    ```

    If the list or tuple argument is omitted, returns a function of the mapper that expects the argument.

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
    """Execute a callback concurrently for each element of a list or tuple.

    A callback is a function that does not necessarily specify a value or return. Each callback invocation happens in a separate thread.

    ```python
    tforeach([1, 2, 3], print)
    ```

    If the list or tuple argument is omitted, returns a function of the callback that expects the argument.

    ```python
    my_foreach_func = tforeach(print)
    my_foreach_func([1, 2, 3])
    ```

    """
    if callable(args[0]):
        return partial(_tforeach, _, args[0])
    return _tforeach(*args)

def _tfilter(argument, func):
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
    index = 0
    while index < length:
        t = threads[index]
        t.join()
        if t.result:
            result.append(argument[index])
        index += 1
    if isinstance(argument, tuple):
        return tuple(result)
    return result

def tfilter(*args):
    """Concurrently filter a list or tuple.

    A predicate is a function that specifies an element of a list or tuple and returns a boolean value. Elements corresponding to predicate invocations that return `False` are filtered out of the resulting list or tuple, while elements corresponding to predicate invocationsn that return `True` are retained. Each predicate invocation happens in a separate thread.

    ```python
    def is_odd(n):
        return n % 2 == 1

    odd_numbers = tfilter([1, 2, 3, 4, 5], is_odd)
    ```

    If the list or tuple argument is omitted, returns a function of the predicate that expects the argument.

    ```python
    def is_odd(n):
        return n % 2 == 1

    filter_odds = tfilter(is_odd)
    odd_numbers = filter_odds([1, 2, 3, 4, 5])
    ```

    """
    if callable(args[0]):
        return partial(_tfilter, _, args[0])
    return _tfilter(*args)

def reduce(*args):
    """Reduce a list or tuple to a single value (accumulator).

    A reducer is a function that specifies an accumulator and a given element of a list or tuple, and returns an accumulator. Each reducer invocation happens sequentially.

    ```python
    # add is a reducer
    def add(a, b):
        return a + b

    sum = reduce([1, 2, 3, 4, 5], add)
    ```

    If an initial value is provided, it is treated as the starting value for the accumulator.

    ```python
    sum = reduce([1, 2, 3, 4, 5], add, 10)
    ```

    If the list or tuple argument is omitted, returns a function of the reducer and initial value that expects the argument.

    ```python
    reducing_func = reduce(add, 10)
    sum = reducing_func([1, 2, 3, 4, 5])
    ```

    """
    if callable(args[0]):
        if len(args) == 2:
            return partial(_reduce, args[0], _, args[1])
        return partial(_reduce, args[0])
    if len(args) == 3:
        return _reduce(args[1], args[0], args[2])
    return _reduce(args[1], args[0])

def _tflatmap(argument, func):
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
        if isinstance(t.result, list) or isinstance(t.result, tuple):
            result = result + t.result
        else:
            result.append(t.result)
    if isinstance(argument, tuple):
        return tuple(result)
    return result

def tflatmap(*args):
    """Apply a flatmapper concurrently to each element of a list or tuple, concatenating the results.

    A flatmapper is a function that specifies an element of the list or tuple, and returns a list, tuple, or single element. A returned list or tuple is concatenated onto the resulting list or tuple, while a returned single element is appended. Each flatmapper invocation happens in a separate thread.

    ```python
    duplicates = tflatmap([1, 2, 3], lambda n: [n, n, n])
    ```

    If the list or tuple argument is omitted, returns a function of the flatmapping function that expects the argument.

    ```python
    my_flatmapping_func = tflatmap(lambda n: [n, n, n])
    duplicates = my_flatmapping_func([1, 2, 3])
    ```

    """
    if callable(args[0]):
        return partial(_tflatmap, _, args[0])
    return _tflatmap(*args)

__name__ = 'functions'

__all__ = ['always', 'thunkify', 'chain', 'tap', 'tmap', 'tforeach', 'tfilter', 'reduce', 'tflatmap']
