# Copyright (c) 2023, Henrik Larsen
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

import inspect
from lib_actors.scheduler import Scheduler


class Timer:
    """
<    The Timer class is a simple implementation of timer function.
    A Timer can be stated and stopped at any time.
    When the timer times out its callback function is called.

    Example:
        timer = Timer(1000, self.func)

        timer.start()
    """

    def __init__(self, msec: int, func):
        """
        Creates a timer. After the timer has been started it will time out after a specified period
        and the callback function will be executed.

        Example:
            timer = Timer(1000, self.func)

            timer.start()

        :param msec: timeout in milliseconds.
        :param func: call back function to be executed when the timer times out.
        """

        self.msec = msec
        self.func = func
        self.cb_func = func
        self.lock = None
        actor = inspect.currentframe().f_back.f_locals["self"]  # Dirty trick to get the Actor instance.
        if hasattr(actor, "lock"):
            self.lock = actor.lock  # Lock from Actor to synchronize callback functions
            self.cb_func = self._locked_func
        self.job_id = None

    def _locked_func(self):
        with self.lock:
            self.func()

    def stop(self):
        """
        Stops a running timer.

        Example:
            timer.stop()
        """

        if self.job_id is not None:
            Scheduler.get_instance().remove(self.job_id)
            self.job_id = None

    def start(self):
        """
        Starts or restarts the timer.

        Example:f_back
            timer.start()
        """

        self.stop()
        self.job_id = Scheduler.get_instance().once(self.msec, self.cb_func)
