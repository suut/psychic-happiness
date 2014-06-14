#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import threading
import time
import sys
import trace
from inspect import isgeneratorfunction


class KillableThread(threading.Thread):
    """A subclass of threading.Thread, with a kill() method provided by courtsey of Connelly Barnes."""
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run      # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class FunctionExecutor(KillableThread):
    def __init__(self, _f: 'the function to execute', _callback, args, kwargs):
        super().__init__()
        self._f = _f
        self._callback = _callback
        self.args = args
        self.kwargs = kwargs

    def run(self):
        ret = self._f(*self.args, **self.kwargs)
        if ret is not None:
            if repr(type(ret)) == '<class \'generator\'>':
                for i in ret:
                    self._callback(i)
            else:  # TODO: make function to be only generators, not normal functions
                print('DEPRECATED: function "', self._f.cmdname, '" is using the return statement', sep='')
                self._callback(ret)


class ControlThread(threading.Thread):
    def __init__(self, _f, _callback, *args, **kwargs):
        super().__init__()
        self.watched_thread = FunctionExecutor(_f, _callback, args, kwargs)
        self._callback = _callback

    def run(self):
        self.watched_thread.start()
        time.sleep(3)
        if self.watched_thread.is_alive():
            self.watched_thread.kill()
            self._callback('timeout')
