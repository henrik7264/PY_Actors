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

import logging
from reactivex import create, Observable
from threading import Lock
from lib_actors.dispatcher import Dispatcher
from lib_actors.scheduler import Scheduler
from lib_actors.timer import Timer


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

        self.message.subscribe(MyMessage, self.sub)

        def sub(self, msg: MyMessage):
            self.logger.debug("Received a MyMessage: " + msg.data)

    or start to publish messages in the following way

        self.scheduler.repeat(1000, self.pub)

        def pub(self):
            self.message.publish(MyMessage("Hello world"))
    """

    def __init__(self, name: str, log_level: int = logging.CRITICAL):
        """
        The initialization of an Actor.

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
        self.message = Actor._Message(self.lock)
        self.scheduler = Actor._Scheduler(self.lock)

    class _Message:
        def __init__(self, lock: Lock):
            """
            Do not create instances of this class!

            Access the scheduler functions using the following constructs:
                self.message.subscribe(...)
                self.message.publish(...)
                self.message.stream(...)
            """
            self.actor_lock = lock

        def subscribe(self, func, msg_type):
            """
            Message function - The Actor will subscribe to the specified message type
            and call the callback function each time a message of the specified type is published


            Example:
                self.message.subscribe(MyMessage, self.func)

                def func(self, msg: MyMessage):
                    self.logger.debug("Received a MyMessage: " + msg.data)

            :param msg_type: A reference to a class/message.
            :param func: A lambda or callback function. The function must take a message argument of the specified type.
            :return
            """
            def _locked_func(msg):
                with self.actor_lock:
                    func(msg)
            return Dispatcher.get_instance().register_cb(_locked_func, msg_type)

        @staticmethod
        def unsubscribe(sub_id, msg_type) -> None:
            Dispatcher.get_instance().unregister_cb(sub_id, msg_type)

        @staticmethod
        def publish(msg) -> None:
            """
            Message function - The Actor will publish the specified message.

            Example:
                self.message.publish(MyMessage("Hello world"))

            :param msg: The message (instance of a class) to be published.
            """
            Dispatcher.get_instance().publish(msg)

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

    class _Scheduler:
        def __init__(self, lock: Lock):
            """
            Do not create instances of this class!

            Access the scheduler functions from an Actor by means of the following constructs:
                self.scheduler.once(...)
                self.scheduler.repeat(...)
                self.scheduler.remove(...)
            """
            self.actor_lock = lock

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
                with self.actor_lock:
                    func()

            return Scheduler.get_instance().once(msec, _locked_func)

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
                with self.actor_lock:
                    func()

            return Scheduler.get_instance().repeat(msec, _locked_func)

        @staticmethod
        def remove(job_id: int):
            """
            Scheduler function - will delete the scheduled job.

            Example:
                job_id = self.scheduler.once(1000, self.func)

                self.scheduler.remove(job_id)

            :param job_id: the job to be removed.
            """
            Scheduler.get_instance().remove(job_id)

        def timer(self, msec: int, func):
            return Timer(self.actor_lock, msec, func)
