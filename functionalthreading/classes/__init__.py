from threading import Thread as _Thread

class Thread(_Thread):
    """Represents an execution that is run in a thread.

    A thread is an independent unit of a process that is scheduled by the operating system's thread scheduler and can be run concurrently.

    After the target invocation, the result of the invocation is stored under the `result` property of the thread.

    ```python
    def f(n):
        return n ** 2

    t = Thread(target=f, args=[3])
    t.start()
    t.join()
    print(t.result)
    ```

    Methods: [start](https://docs.python.org/3/library/threading.html#threading.Thread.start), [join](https://docs.python.org/3/library/threading.html#threading.Thread.start)

    """
    def __init__(self, **kwargs):
        """The constructor should always be called with keyword arguments. Arguments are:

        target - the callable object to be invoked.

        args - a list or tuple of arguments for the target invocation.

        kwargs - a dictionary of keyword arguments for the target invocation.

        daemon - explicitly sets whether the thread is daemonic. If `None` (the default), the daemonic property is inherited from the current thread.

        """
        _Thread.__init__(self, **kwargs)
        self.result = None
        self._target = kwargs['target']
        self._args = ()
        self._kwargs = {}
        if 'args' in kwargs:
            self._args = kwargs['args']
        if 'kwargs' in kwargs:
            self._kwargs = kwargs['kwargs']

    def run(self):
        self.result = self._target(*self._args, **self._kwargs)

__name__ = 'classes'

__all__ = ['Thread']
