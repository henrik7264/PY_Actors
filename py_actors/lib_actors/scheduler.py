# Copyright (c) 2023, Henrik Larsen
# https://github.com/henrik7264/PY_Actors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from time import time
from threading import Thread, Event, Lock
from lib_actors.executor import Executor


class Scheduler(Thread):
    """
    The Scheduler class schedules jobs (callback functions) to be executed at a specific time.
    The Scheduler supports jobs to be executed only one time or repeatedly.

    A dictionary is used to store all information about the scheduled jobs.
    The dictionary is walked through to determine if there are any jobs to be executed.
    If so, the jobs will be executed immediately. If not, the scheduler will wait until
    the next job is scheduled to be executed.

    The Scheduler makes use of a number of Workers to execute the callback functions.
    The number of workers will adapt to the load of the Scheduler. When the size of the
    worker queue exceeds a given number a new worker will be created.
    """

    __instance__ = None  # A Scheduler is a singleton.

    def __init__(self):
        """
        Do not create instances of this class! Scheduler is a singleton.
        """
        super().__init__(daemon=True)
        self.job_id = 0  # unique id that is returned each time a job is scheduled.
        self.jobs = {}  # { job_id1: (timeout1, msec1, f1, repeat1), job_id2: (timeout2, msec2, f2, repeat2), ...}
        self.executor = Executor.get_instance()  # Execute functions
        self.event = Event()  # Control if the wait should be blocked or not
        self.lock = Lock()  # Synchronize critical regions/data.
        self.start()

    @staticmethod
    def get_instance():
        """
        The Scheduler is a singleton and should only be accessed through this function.

        Example:
            scheduler = Scheduler.get_instance()

        :return: an instance of the Scheduler class.
        """
        if Scheduler.__instance__ is None:
            Scheduler.__instance__ = Scheduler()
        return Scheduler.__instance__

    def run(self):
        while True:
            if len(self.jobs) == 0:
                self.event.wait()
                self.event.clear()
            else:
                next_timeout = sys.float_info.max
                with self.lock:
                    for job_id, (job_timeout, job_msec, job_func, job_repeat) in self.jobs.items():
                        if job_repeat > 0 and job_timeout < next_timeout:
                            next_timeout = job_timeout
                current_time = time()
                if next_timeout > current_time:
                    self.event.wait(timeout=next_timeout-current_time)
                    self.event.clear()

            current_time = time()
            with self.lock:
                for job_id, (job_timeout, job_msec, job_func, job_repeat) in self.jobs.items():
                    if job_repeat > 0 and job_timeout <= current_time:
                        self.executor.exec(job_func)
                        self.jobs[job_id] = (job_timeout+float(job_msec)/1000.0, job_msec, job_func, job_repeat-1)

    def once(self, msec: int, func) -> int:
        """
        Starts a scheduler that after the specified timeout will execute the call back function.

        Example:
            job_id = scheduler.once(1000, self.func)

        :param msec: timeout in milliseconds.
        :param func: call back function to be executed when the job times out.
        :return: job_id
        """
        with self.lock:
            self.job_id += 1
            self.jobs[self.job_id] = (time()+float(msec)/1000.0, msec, func, 1)
            self.event.set()
            return self.job_id

    def repeat(self, msec: int, func) -> int:
        """
        Starts a scheduler that repeatedly at every timeout will execute the call back function.

        Example:
            job_id = scheduler.repeat(1000, self.func)

        :param msec: timeout in milliseconds.
        :param func: call back function to be executed when the job times out.
        :return: job id
        """
        with self.lock:
            self.job_id += 1
            self.jobs[self.job_id] = (time()+float(msec)/1000.0, msec, func, sys.maxsize)
            self.event.set()
            return self.job_id

    def remove(self, job_id: int):
        """
        Stops and removes a scheduled job.

        Example:
            job_id = scheduler.once(1000, self.func)

            self.scheduler.remove(job_id)

        :param job_id: the job to be removed.
        """
        with self.lock:
            if self.jobs.get(job_id) is not None:
                self.jobs.pop(job_id)
                self.event.set()
