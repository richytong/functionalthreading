# functionalthreading
functionalthreading - Concurrent functional programming with thread-based parallelism

```python
from functionalthreading import chain, tap, tmap

chain(
    (0, 1, 2),
    tmap(lambda n: n + 1),
    tap(print),
    tmap(lambda n: n ** 2),
    print
)
```

## Introduction
The functionalthreading module provides functions for concurrent functional programming with thread-based parallelism. Functional programming is a programming paradigm where a program is thought to be a tree of functions. This module offers functions and classes that enable the functional programming paradigm and concurrent programming in Python.

## Functional Programming
See [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html).

## Reference

### Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, context=None)
Represents an execution that is run in a thread.

A thread is an independent unit of a process that is scheduled by the operating system's thread scheduler and can be run concurrently.

Once a thread object is created, its activity must be started by calling the thread’s start() method. This invokes the run() method in a separate thread of control.

Once the thread’s activity is started, the thread is considered ‘alive’. It stops being alive when its run() method terminates – either normally, or by raising an unhandled exception. The is_alive() method tests whether the thread is alive.

Other threads can call a thread’s join() method. This blocks the calling thread until the thread whose join() method is called is terminated.

A thread has a name. The name can be passed to the constructor, and read or changed through the name attribute.

If the run() method raises an exception, threading.excepthook() is called to handle it. By default, threading.excepthook() ignores silently SystemExit.

A thread can be flagged as a “daemon thread”. The significance of this flag is that the entire Python program exits when only daemon threads are left. The initial value is inherited from the creating thread. The flag can be set through the daemon property or the daemon constructor argument.

> Note: Daemon threads are abruptly stopped at shutdown. Their resources (such as open files, database transactions, etc.) may not be released properly. If you want your threads to stop gracefully, make them non-daemonic and use a suitable signalling mechanism such as an Event.

There is a “main thread” object; this corresponds to the initial thread of control in the Python program. It is not a daemon thread.

There is the possibility that “dummy thread objects” are created. These are thread objects corresponding to “alien threads”, which are threads of control started outside the threading module, such as directly from C code. Dummy thread objects have limited functionality; they are always considered alive and daemonic, and cannot be joined. They are never deleted, since it is impossible to detect the termination of alien threads.

After the target invocation, the result of the invocation is stored under the `result` property of the thread.

```python
def f(n):
    return n ** 2

t = Thread(target=f, args=[3])
t.start()
t.join()
print(t.result)
```


#### start()
Start the thread’s activity.

It must be called at most once per thread object. It arranges for the object’s run() method to be invoked in a separate thread of control.

This method will raise a RuntimeError if called more than once on the same thread object.

If supported, set the operating system thread name to threading.Thread.name. The name can be truncated depending on the operating system thread name limits.

> Changed in version 3.14: Set the operating system thread name.

#### run()
Method representing the thread’s activity. This method does not need to be called.

#### join(timeout=None)
Wait until the thread terminates. This blocks the calling thread until the thread whose join() method is called terminates – either normally or through an unhandled exception – or until the optional timeout occurs.

When the timeout argument is present and not None, it should be a floating-point number specifying a timeout for the operation in seconds (or fractions thereof). As join() always returns None, you must call is_alive() after join() to decide whether a timeout happened – if the thread is still alive, the join() call timed out.

When the timeout argument is not present or None, the operation will block until the thread terminates.

A thread can be joined many times.

join() raises a RuntimeError if an attempt is made to join the current thread as that would cause a deadlock. It is also an error to join() a thread before it has been started and attempts to do so raise the same exception.

If an attempt is made to join a running daemonic thread in late stages of Python finalization join() raises a PythonFinalizationError.

> Changed in version 3.14: May raise PythonFinalizationError.

#### name
A string used for identification purposes only. It has no semantics. Multiple threads may be given the same name. The initial name is set by the constructor.

On some platforms, the thread name is set at the operating system level when the thread starts, so that it is visible in task managers. This name may be truncated to fit in a system-specific limit (for example, 15 bytes on Linux or 63 bytes on macOS).

Changes to name are only reflected at the OS level when the currently running thread is renamed. (Setting the name attribute of a different thread only updates the Python Thread object.)

#### getName()
#### setName()
Deprecated getter/setter API for name; use it directly as a property instead.

> Deprecated since version 3.10.

#### ident
The ‘thread identifier’ of this thread or None if the thread has not been started. This is a nonzero integer. See the get_ident() function. Thread identifiers may be recycled when a thread exits and another thread is created. The identifier is available even after the thread has exited.

#### native_id
The Thread ID (TID) of this thread, as assigned by the OS (kernel). This is a non-negative integer, or None if the thread has not been started. See the get_native_id() function. This value may be used to uniquely identify this particular thread system-wide (until the thread terminates, after which the value may be recycled by the OS).

> Note: Similar to Process IDs, Thread IDs are only valid (guaranteed unique system-wide) from the time the thread is created until the thread has been terminated.

Availability: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX, DragonFlyBSD.

> Added in version 3.8.

#### is_alive()
Return whether the thread is alive.

This method returns `True` just before the run() method starts until just after the run() method terminates. The module function enumerate() returns a list of all alive threads.

#### daemon
A boolean value indicating whether this thread is a daemon thread (`True`) or not (`False`). This must be set before start() is called, otherwise RuntimeError is raised. Its initial value is inherited from the creating thread; the main thread is not a daemon thread and therefore all threads created in the main thread default to `daemon = False`.

#### isDaemon
#### setDaemon
Deprecated getter/setter API for daemon; use it directly as a property instead.

> Deprecated since version 3.10.

### partial(func, /, *args, **keywords)
Create a new function with partial application of the given arguments
and keywords. If more arguments are supplied to the call, they are appended to args. If additional keyword arguments are supplied, they extend and override keywords. Roughly equivalent to:

```python
def partial(func, /, *args, **keywords):
    def newfunc(*more_args, **more_keywords):
        return func(*args, *more_args, **(keywords | more_keywords))
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```

The partial() function is used for partial function application which “freezes” some portion of a function’s arguments and/or keywords resulting in a new object with a simplified signature. For example, partial() can be used to create a callable that behaves like the int() function where the base argument defaults to 2:

```python
>>> basetwo = partial(int, base=2)
>>> basetwo.__doc__ = 'Convert base 2 string to an int.'
>>> basetwo('10010')
18
```

If _ (Placeholder) sentinels are present in args, they will be filled first when partial() is called. This makes it possible to pre-fill any positional argument with a call to partial(); without _, only the chosen number of leading positional arguments can be pre-filled.

If any _ sentinels are present, all must be filled at call time:

```python
>>> say_to_world = partial(print, _, _, "world!")
>>> say_to_world('Hello', 'dear')
Hello dear world!
```

If partial is applied to an existing `partial()` object, _ sentinels of the input object are filled in with new positional arguments. _ can be retained by inserting a new _ sentinel to the place held by a previous _:

```python
>>> from functools import partial, Placeholder as _
>>> remove = partial(str.replace, _, _, '')
>>> message = 'Hello, dear dear world!'
>>> remove(message, ' dear')
'Hello, world!'
>>> remove_dear = partial(remove, _, ' dear')
>>> remove_dear(message)
'Hello, world!'
>>> remove_first_dear = partial(remove_dear, _, 1)
>>> remove_first_dear(message)
'Hello, dear world!'
```

Placeholder cannot be passed to partial() as a keyword argument.

> Changed in version 3.14: Added support for Placeholder in positional arguments.

### _ (Placeholder)
The type of the Placeholder singleton.

Used as a placeholder for partial arguments.

> Added in version 3.14.

### always(argument)
Always return a value.

```python
always5 = always(5)

always5()
```


### thunkify(func, *args, **kwargs)
Create a thunk from a function and arguments.

A thunk is a function that takes no arguments and executes the provided function with the provided arguments each call.

```python
printHello = thunkify(print, 'Hello')

printHello()
printHello()
printHello()
```


### chain(*funcs)
### chain(argument, *funcs)
Chain functions together.

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


### tap(func)
Call a function with an argument, returning the argument.

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


### tmap(func)
### tmap(argument, func)
Map a function concurrently across each element of an array or tuple.

Each function invokation happens in a separate thread.

```python
squared = tmap([1, 2, 3], lambda n: n ** 2)
```

If the array or tuple argument is omitted, returns a function of the mapping function that expects the non-function argument.

```python
my_mapping_func = tmap(lambda n: n ** 2)
squared = my_mapping_func([1, 2, 3])
```


