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

import logging
from rx import create, Observable
from threading import Lock
from lib_actors.scheduler import Scheduler
from lib_actors.dispatcher import Dispatcher
from lib_actors.statemachine import Statemachines

logging.basicConfig(level=logging.NOTSET,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler(filename="actors.log", mode="w"), logging.StreamHandler()])


class Actor:
    """
    The Actor class is the most central class of this library.
    An actor is a facade to message handling, scheduling, logging etc.
    All Actor implementations should always be a subclass of the Actor class.
    Use the following construction to create new Actors:

    class MyActor(Actor):
        def __init__(self):
            super().__init__("MyActor", logging.NOTSET)

    The MyActor class can now subscribe to specific messages in the following way:

        self.message.subscribe(MyMessage, self.func)

        def func(self, msg: MyMessage):
                self.logger.debug("Received a MyMessage: " + msg.data)

    or start to publish messages in the following way

        self.scheduler.repeat(1000, self.message.publish(MyMessage("Hello world")))
    """

    def __init__(self, name: str, log_level: int = logging.CRITICAL):
        """
        The constructor of an Actor.

        Example:
            class MyActor(Actor):
                def __init__(self):
                    super().__init__("MyActor", logging.NOTSET)

        :param name: The name of the Actor. It must be a unique name that is easy to indentify in log message.
        :param log_level: The default log level is set to CRITICAL. Set it to logging.NOTSET to log everything.
        """
        self.lock = Lock()  # To ensure that call back functions are thread safe.
        self.name = name
        self.logger = logging.getLogger(name) 
        self.logger.setLevel(log_level)
        self.message = Actor.Message(self.lock)
        self.scheduler = Actor.Scheduler(self.lock)

    class Scheduler:
        def __init__(self, lock: Lock):
            """
            Do not create instances of this class!

            Access the scheduler functions from an Actor by means of the following constructs:
                self.scheduler.once(...)
                self.scheduler.repeat(...)
                self.scheduler.remove(...)
            """
            self.lock = lock
            self.scheduler = Scheduler.get_instance()

        def once(self, msec: int, func) -> int:
            """
            Scheduler function - will after the specified timeout execute the call back function.

            Example:
                job_id = self.scheduler.once(1000, self.func)

            :param msec: timeout in milliseconds.
            :param func: call back function to be executed when the job times out.
            :return: job_id
            """
            def _locked_func():
                with self.lock:
                    func()
            return self.scheduler.once(msec, _locked_func)

        def repeat(self, msec: int, func) -> int:
            """
            Scheduler function - will repeatedly at every timeout execute the call back function.

            Example:
                job_id = self.scheduler.repeat(1000, self.func)

            :param msec: timeout in milliseconds.
            :param func: call back function to be executed when the job times out.
            :return: job id
            """
            def _locked_func():
                with self.lock:
                    func()
            return self.scheduler.repeat(msec, _locked_func)

        def remove(self, job_id: int):
            """
            Scheduler function - will delete the scheduled job.

            Example:
                job_id = self.scheduler.once(1000, self.func)

                self.scheduler.remove(job_id)

            :param job_id: the job to be removed.
            """
            self.scheduler.remove(job_id)

    class Message:
        def __init__(self, lock: Lock):
            """
            Do not create instances of this class!

            Access the scheduler functions using the following constructs:
                self.message.subscribe(...)
                self.message.publish(...)
                self.message.stream(...)
            """
            self.lock = lock
            self.msg_dispatcher = Dispatcher.get_instance()
            self.sm_dispatcher = Statemachines.get_instance()

        def subscribe(self, msg_type, func) -> None:
            """
            Message function - The Actor will subscribe to the specified message type
            and call the callback function each time a message of the specified type is published

            Example:
                self.message.subscribe(MyMessage, self.func)

                def func(self, msg: MyMessage):
                    self.logger.debug("Received a MyMessage: " + msg.data)

            :param msg_type: A reference to a class/message.
            :param func: A lambda or callback function. The function must take a message argument of the specified type.
            """
            def _locked_func(msg):
                with self.lock:
                    func(msg)
            self.msg_dispatcher.subscribe(msg_type, _locked_func)

        def publish(self, msg) -> None:
            """
            Message function - The Actor will publish the specified message.

            Example:
                self.message.publish(MyMessage("Hello world")

            :param msg: The message (instance of a class) to be published.
            """
            self.msg_dispatcher.publish(msg)
            self.sm_dispatcher.message_queue.put(msg)

        def stream(self, msg_type) -> Observable:
            """
            Message function - This function will return a rx.Observable stream
            of messages of the specified message type.

            Example:
                observable = self.message.stream(MyMessage)
                observable.subscribe(...)

            :param msg_type: A reference to a class/message.
            """
            def _stream(observer, scheduler=None):
                self.subscribe(msg_type, lambda msg: observer.on_next(msg))
                return observer
            return create(_stream)
