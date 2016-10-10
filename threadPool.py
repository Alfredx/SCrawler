# -*- coding: utf-8 -*-
# author: ShenChao

import uuid
from threading import Thread, Lock


class Worker(Thread):
    STATE_STOP = 0
    STATE_RUN = 1

    def __init__(self, pool):
        super(Worker, self).__init__()
        self.state = self.STATE_STOP
        self.id = str(uuid.uuid4())
        self.pool = pool
        self.func = None
        self.loops = 0
        self.func_args = ()
        self.func_kwargs = {}

    def set(self, func, loops, *args, **kwargs):
        self.func = func
        self.loops = loops
        self.func_args = args
        self.func_kwargs = kwargs

    def stop(self):
        self.state = self.STATE_STOP

    def run(self):
        self.state = self.STATE_RUN
        loop_count = 0
        while self.state == self.STATE_RUN:
            if not self.func(*self.func_args, **self.func_kwargs):
                break
            if self.loops != 0 and loop_count >= self.loops:
                break


class ThreadPool(object):
    """docstring for ThreadPool"""

    def __init__(self, initNum=0):
        super(ThreadPool, self).__init__()
        self.pool = {}
        self.initNum = initNum

    def startTask(self, func, workers=1, loops=0, func_args=(), func_kwargs={}):
        for i in range(workers):
            new_workder = Worker(self)
            self.pool[new_workder.id] = new_workder
            func_kwargs['task_seq'] = i
            func_kwargs['task_total'] = workers
            new_workder.set(func, loops, *func_args, **func_kwargs)
            new_workder.start()
