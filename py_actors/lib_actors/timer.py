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

from threading import Lock
from lib_actors.scheduler import Scheduler


class Timer:
    """
    Do not create instances of this class!

    Access the timer functions using the following constructs:
        t1 = self.scheduler.timer(...)
        t1.start()
        t1.stop()
    """

    def __init__(self, actor_lock: Lock, msec: int, func):
        self.actor_lock = actor_lock
        self.timer_lock = Lock()
        self.msec = msec
        self.func = func
        self.job_id = None

    def _stop(self):
        if self.job_id is not None:
            Scheduler.get_instance().remove(self.job_id)
            self.job_id = None

    def start(self):
        """
        Starts or restarts the timer.

        Example:
            t1.start()
        """
        def _locked_func():
            with self.actor_lock:
                self.func()

        with self.timer_lock:
            self._stop()
            self.job_id = Scheduler.get_instance().once(self.msec, _locked_func)

    def stop(self):
        """
        Stops a running timer.

        Example:
            t1.stop()
        """
        with self.timer_lock:
            self._stop()
