from threading import Thread as _Thread

class Thread(_Thread):
    """Represents an execution that is run in a thread.

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

    """
    def __init__(self, **kwargs):
        """The constructor should always be called with keyword arguments. Arguments are:

        target - the callable object to be invoked.

        args - a list or tuple of arguments for the target invocation.

        kwargs - a dictionary of keyword arguments for the target invocation.

        daemon - explicitly sets whether the thread is daemonic. If `None` (the default), the daemonic property is inherited from the current thread.

        context - the Context value to use when starting the thread. The default value is `None` which indicates that the sys.flags.thread_inherit_context flag controls the behaviour. If the flag is true, threads will start with a copy of the context of the caller of start(). If false, they will start with an empty context. To explicitly start with an empty context, pass a new instance of Context(). To explicitly start with a copy of the current context, pass the value from copy_context(). The flag defaults true on free-threaded builds and false otherwise.

        > Changed in version 3.3: Added the daemon parameter.

        > Changed in version 3.10: Use the target name if name argument is omitted.

        > Changed in version 3.14: Added the context parameter.

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
