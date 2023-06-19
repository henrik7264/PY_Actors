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

from threading import Lock
from lib_actors.executor import Executor


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
        self.functions_dict = {}  # List of functions/callbacks for each message type {Type1: [cb1, cb2], Type2: [cb3]}
        self.executor = Executor.get_instance()  # Executes the functions.

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

    def subscribe(self, msg_type, func):
        """
        An Actor can subscribe to a message and get a callback function executed each time a message is published.

        Example:
            dispatcher.subscribe(MyMessage, self.func)

            def func(self, msg: MyMessage):
                self.logger.debug("Received a MyMessage: " + msg.data)

        :param msg_type: A reference to a class/message.
        :param func: A lambda or callback function. The function must take a message argument of the specified type.
        """
        with self.lock:
            func_list = self.functions_dict.get(msg_type)
            if func_list is None:
                func_list = []
            func_list.append(func)
            self.functions_dict[msg_type] = func_list

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
            function_list = self.functions_dict.get(type(msg))
            if function_list is not None:
                for func in function_list:
                    self.executor.exec(func, msg)
