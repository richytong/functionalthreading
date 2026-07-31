from threading import Thread as _Thread

class Thread(_Thread):
    def __init__(self, *args, **kwargs):
        _Thread.__init__(self, *args, **kwargs)
        self.value = None
        self.target = kwargs['target']
        self.args = kwargs['args']

    def run(self):
        self.value = self.target(*self.args)

__name__ = 'classes'

__all__ = ['Thread']
