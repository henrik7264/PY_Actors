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

import os
from queue import Queue
from threading import Thread, Lock

class Worker(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.worker_queue = Queue()
        self.start()

    def run(self):
        while True:
            func, arg = self.worker_queue.get()
            func(arg)


Workers = []
No_Workers = os.cpu_count()
for i in range(No_Workers):  # Start the workers.
    Workers.append(Worker())


class Dispatcher:
    """
    The Dispatcher is a helper class to Actors and should as such never be used directly!

    The Dispatcher class handles subscriptions and publish of messages.
    Each subscription is stored in a dictionary where each message type is
    associated to a number of callback functions.

    When a message is published the associated call back functions are looked up
    and executed with the message as argument.

    The publish function makes use of a number of Workers to execute the functions.
    The number of workers will adapt to the load of the incoming messages.
    When the size of the worker queue exceeds a given number a new worker will be created.
    """

    __instance__ = None  # A Dispatcher is a singleton.

    def __init__(self):
        """
        Do not create instances of this class! Dispatcher is a singleton.
        """
        self.lock = Lock()  # To ensure that subscribe and publish function are executed in a thread safe manner
        self.cb_dict = {}  # List of functions/callbacks for each message type {Type1: {id1: cb1, id2: cb2}, Type2: {id3: cb3}}

    @staticmethod
    def get_instance():
        """
        The Dispatcher is a singleton and should only be accessed through this function.

        Example:
            dispatcher = Dispatcher.get_instance()

        :return: an instance of the Dispatcher class.
        """
        if Dispatcher.__instance__ is None:
            Dispatcher.__instance__ = Dispatcher()
        return Dispatcher.__instance__

    def register_cb(self, func, msg_type):
        """
        An Actor can subscribe to a message and get a callback function executed each time a message is published.

        Example:
            dispatcher.register_cb(self.func, MyMessage)

            def func(self, msg: MyMessage):
                self.logger.debug("Received a MyMessage: " + msg.data)

        :param msg_type: A reference to a class/message.
        :param func: A lambda or callback function. The function must take a message argument of the specified type.
        """
        with self.lock:
            func_id = id(func)
            func_dict = self.cb_dict.get(msg_type)
            if func_dict is None:
                self.cb_dict[msg_type] = {func_id: func}
            else:
                func_dict[func_id] = func
            return func_id

    def unregister_cb(self, func_id, msg_type):
        with self.lock:
            func_dict = self.cb_dict.get(msg_type)
            if func_dict is not None:
                func_dict.pop(func_id)
                if not func_dict:
                    self.cb_dict.pop(msg_type)

    def publish(self, msg):
        """
        The publish function will look up the callback functions
        that is associated to the message type (subscriptions)
        and execute each function with the message as argument.
        The actual execution is performed by the Workers of the Dispatcher class.

        Example:
            dispatcher.publish(MyMessage("Hello world"))

        :param msg: The message (instance of a class) to be published.
        """
        with self.lock:
            msg_type = type(msg)
            func_dict = self.cb_dict.get(msg_type)
            if func_dict is not None:
                worker = Workers[id(msg_type) % No_Workers]
                for func in func_dict.values():
                    worker.worker_queue.put((func, msg))
