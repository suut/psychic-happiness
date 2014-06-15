#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import threading
import time
import sys
import trace


def callback(ret):
    print('callback called with argument', ret)


def f():
    return 'zizi'


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
    def __init__(self, f: 'the function to execute'):
        super().__init__()
        self._f = f

    def run(self, *args, **kwargs):
        self.result = self._f(*args, **kwargs)


class ControlThread(threading.Thread):
    def __init__(self, f):
        super().__init__()
        self.watched_thread = FunctionExecutor(f)

    def run(self):
        self.watched_thread.start()
        time.sleep(3)
        if self.watched_thread.is_alive():
            self.watched_thread.kill()
            print('timeout.')

