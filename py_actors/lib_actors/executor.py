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

from queue import Queue
from threading import Thread


class Executor:
    __instance__ = None  # An Executor is a singleton.

    class Worker(Thread):
        def __init__(self, worker_queue: Queue):
            super().__init__(daemon=True)
            self.worker_queue = worker_queue  # Shared queue with Executor
            self.start()

        def run(self):
            while True:
                func, arg = self.worker_queue.get()
                if arg is None:
                    func()
                else:
                    func(arg)

    def __init__(self):
        self.worker_queue = Queue()  # queue of functions and messages to be executed.
        self.worker_queue_max_size = 2  # When the queue exceeds this size a new Worker will be created
        self.workers = [Executor.Worker(self.worker_queue)]  # List of workers

    @staticmethod
    def get_instance():
        if Executor.__instance__ is None:
            Executor.__instance__ = Executor()
        return Executor.__instance__

    def exec(self, func, arg=None):
        self.worker_queue.put((func, arg))
        if self.worker_queue.qsize() > self.worker_queue_max_size:
            self.workers.append(Executor.Worker(self.worker_queue))
            self.worker_queue_max_size *= 2
