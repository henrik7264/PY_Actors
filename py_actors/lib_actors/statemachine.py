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

from typing import cast
from enum import Enum
from queue import Queue
from threading import Thread
from lib_actors.scheduler import Scheduler


class TransitionType(Enum):
    MESSAGE = 0
    TIMER = 1


class Transition:
    """
    A statemachine is defined by an initial state and a number of states it can change to at any given time:

    self.sm = Statemachine(Initial_state,
                    State(State_1,
                        Transition(...),
                        Transition(...)),
                    State(State_n,
                        Transition(...),
                        Transition(...)))

    Each State defines a number of Transitions that allows the statemachine to change from one state to another.
    A transition is identified by a trigger, an action and a next_state operation. The trigger can either be a
    message or a timer. The action is a callback function that is executed each time the transition is triggered.
    The transition will finally change the state of the statemachine to the specified next_state.
    """

    def __init__(self, trans_type: TransitionType, action=None, next_state=None):
        """
        Each State defines a number of Transitions that allow the statemachine to change from one state to another.
        A transition is identified by a trigger, an action and a next state operation. The trigger can either be a
        message or a timer. The action is a callback function that is executed each time the transition is triggered.
        The transition will finally change the state of the statemachine to the specified in next_state.

        Example:
            class States(Enum):
                DOOR_OPENED = 0,
                DOOR_CLOSED = 1
            self.sm = Statemachine(self, States.DOOR_CLOSED,
                           State(States.DOOR_CLOSED,
                                 MessageTrans(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 MessageTrans(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 TimerTrans(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param trans_type: The type of the transition, either a Message or Timer.
        :param action: A callback function that is executed each time a transition is triggered.
        :param next_state: The next state of the statemachine. Set as part of a transition is triggered.
        """
        self.statemachine = None
        self.trans_type = trans_type
        self.action = action
        self.next_state = next_state

    def set_statemachine(self, statemachine):
        """
        Internal function - do not use!

        Sets the statemachine, so the current state of statemachine can be updated as part of a transition.

        :param statemachine: A Statemachine.
        :return:
        """
        self.statemachine = statemachine


class MessageTrans(Transition):
    """
    A MessageTrans is a transition that is triggered by a message published by an Actor.
    """

    def __init__(self, msg_type, action=None, next_state=None):
        """
        A MessageTrans is a transition that is triggered by a message published by an Actor.

        The MessageTrans must specify the exact message type that triggers the transition.
        It must also specify an action which is a callback function that called each time the transition is triggered.
        Finally, it must specify a next state which the statemachine will be in the transition is complete.

        Example:
            MessageTrans(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),

        :param msg_type: The specific message type that will trigger the transition.
        :param action: A callback function that is executed when the transition is triggered.
        :param next_state: The next state of the statemachine when then transition is complete.
        """
        super().__init__(trans_type=TransitionType.MESSAGE, action=action, next_state=next_state)
        self.msg_type = msg_type

    def update(self, msg):
        """
        Internal function - do not use.

        Actual execution of the action callback function of the transition.

        :param msg: A message published by an Actor.
        """
        with self.statemachine.lock:
            if self.action is not None:
                self.action(msg)
            self.statemachine.set_current_state(self.next_state)


class TimerTrans(Transition):
    """
    A TimerTrans is a transition that is triggered by a timer when it times out.
    """

    def __init__(self, timeout: int, action=None, next_state=None):
        """
        A TimerTrans is a transition that is triggered by a timer when it times out.

        The TimerTrans must specify the timeout of the timer.
        It must also specify an action which is a callback function that called when the timer times out.
        Finally, it must specify a next state which the statemachine will be in the transition is complete.

        Example:
            TimerTrans(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)),

        :param timeout: The timeout in milliseconds. When the timer times out the transition will be triggered.
        :param action: A callback function that is executed when the transition is triggered.
        :param next_state: The next state of the statemachine when then transition is complete.
        """
        super().__init__(trans_type=TransitionType.TIMER, action=action, next_state=next_state)
        self.timeout = timeout

    def update(self):
        """
        Internal function - do not use.

        Actual execution of the action callback function of the transition.
        """
        with self.statemachine.lock:
            if self.action is not None:
                self.action()
            self.statemachine.set_current_state(self.next_state)


class State:
    """
    A statemachine is defined by an initial state and then a number of states it can change to at any given time:

    self.sm = Statemachine(Initial_state,
                    State(State_1,
                        Transition(...),
                        Transition(...)),
                    State(State_n,
                        Transition(...),
                        Transition(...)))

    Each State defines a number of Transitions that allow the statemachine to change from one state to another.
    The trigger is either a Message or Timer.
    """

    def __init__(self, state_name, *transitions: Transition):
        """
        Each State defines a number of Transitions that allow the statemachine to change from one state to another.
        The trigger of a transition is either a Message or Timer.

        Example:
            class States(Enum):
                DOOR_OPENED = 0,
                DOOR_CLOSED = 1
            self.sm = Statemachine(self, States.DOOR_CLOSED,
                           State(States.DOOR_CLOSED,
                                 MessageTrans(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 MessageTrans(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 TimerTrans(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param state_name: The name of a State, typically an enum, i.e. integer.
        :param transitions: A number of transitions that when triggered will change the state of the statemachine.
        """
        self.state_name = state_name  # typically an enum, i.e. integer
        self.transitions = transitions  # The transitions of a state
        self.message_dict = {}  # {MsgType1: Trans1, MsgType2: Trans2, ...}
        self.timers_list = []  # [Trans3, Trans4 ...]
        for trans in self.transitions:
            if trans.trans_type == TransitionType.MESSAGE:
                message_trans = cast(MessageTrans, trans)
                self.message_dict[message_trans.msg_type] = message_trans
            elif trans.trans_type == TransitionType.TIMER:
                timer_trans = cast(TimerTrans, trans)
                self.timers_list.append(timer_trans)

    def set_statemachine(self, statemachine):
        """
        Internal function - do not use!

        Forwards the statemachine instance to all transitions.

        :param statemachine: A Statemachine.
        """
        for trans in self.transitions:
            trans.set_statemachine(statemachine)

    def update(self, msg):
        """
        Internal function - do not use!

        The function works as follows: The Statemachine will call this function with a message
        that has been published by an Actor. update will then look up the transition that is triggered
        by this message and calls its update function.

        :param msg: A message published by an Actor.
        """
        trans = self.message_dict.get(type(msg))
        if trans is not None:
            trans.update(msg)


class Statemachine:
    """
    A Statemachine is defined as follows (ref. https://en.wikipedia.org/wiki/Finite-state_machine):
        It is an abstract machine that can be in exactly one of a finite number of states at any given time.
        The Finite State Machine can change from one state to another in response to some inputs;
        the change from one state to another is called a transition.

    A statemachine is defined by an initial state and then a number of states it can change to at any given time:

    self.sm = Statemachine(Initial_state,
                    State(State_1,
                        Transition(...),
                        Transition(...)),
                    State(State_n,
                        Transition(...),
                        Transition(...)))

    Each State defines a number of Transitions that allow the statemachine to change from one state to another.
    The trigger of a transition is either a Message or Timer.
    """

    def __init__(self, actor, initial_state, *states: State):
        """
        A statemachine is defined by an initial state and a number of states it can change to at any given time

        Example:
            class States(Enum):
                DOOR_OPENED = 0,
                DOOR_CLOSED = 1
            self.sm = Statemachine(self, States.DOOR_CLOSED,
                           State(States.DOOR_CLOSED,
                                 MessageTrans(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 MessageTrans(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 TimerTrans(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param actor: The Actor that defines the statemachine. Needed to get the lock of the Actor.
        :param initial_state: The initial state of the Statemachine
        :param states: A number of states of the statemachine.
        """
        self.lock = actor.lock  # Shared lock with Actor
        self.current_state = None  # Current state of the Statemachine, typically an enum, i.e. integer
        self.states = states  # The states of a statemachine
        self.state_dict = {}  # { name1: State1, name2: State2, ...}, name is typically an enum, i.e. integer
        self.scheduler = Scheduler.get_instance()  # Scheduler instance
        self.scheduled_jobs = []  # [job_id1, job_id2, ...]
        for state in self.states:
            state.set_statemachine(self)
            self.state_dict[state.state_name] = state
        self.set_current_state(initial_state)
        Statemachines.get_instance().register(self)

    def get_current_state(self):
        """
        Returns the current state of a statemachine.

        Example:
            self.curr_state = self.statemachine.get_current_state()

        :return: Current state of the statemachine. Typically, an enum or integer.
        """
        return self.current_state

    def set_current_state(self, new_state):
        """
        Internal function - do not use!

        The function sets the current state of the statemachine.
        Only a Transition should set the current state of the statemachine.

        :param new_state: The new/current state of the statemachine.
        """
        for job_id in self.scheduled_jobs:
            self.scheduler.remove(job_id)
        self.scheduled_jobs = []
        if new_state is not None:
            self.current_state = new_state
        state = self.state_dict.get(self.current_state)
        if state is not None:
            for trans in state.timers_list:
                timer_trans = cast(TimerTrans, trans)
                self.scheduled_jobs.append(self.scheduler.once(timer_trans.timeout, timer_trans.update))

    def update(self, msg):
        """
        Internal function - do not use!

        The update function works as follows: A Worker of the Statemachines class calls update
        with a message that has been published by an Actor. Update will pass this message
        to the current State by calling its update function.

        :param msg: A message published by an Actor.
        """
        state = self.state_dict.get(self.current_state)
        if state is not None:
            state.update(msg)


class Statemachines(Thread):
    """
    The Statemachines class keeps track of all created statemachines.

    Each statemachine must register itself calling the register function.
    Part of registration is to walk through the statemachine and associate
    each transition that is triggered by message to the statemachine. This
    will allow for easy look up of statemachines that should be updated
    when a message is published.

    The Statemachines class makes use of a number of Workers to execute the actions of a transition.
    The number of workers will adapt to the load of the messages. When the size of the worker queue
    exceeds a given number a new worker will be created.
    """

    __instance__ = None  # A Statemachines class is a singleton.

    class Worker(Thread):
        """
        The Worker class takes care of executing the (update function, statemachine) pair that is pushed to its queue.
        """
        def __init__(self, worker_queue: Queue):
            super().__init__(daemon=True)
            self.worker_queue = worker_queue  # Shared queue with statemachines
            self.start()

        def run(self):
            while True:
                update, sm = self.worker_queue.get()
                update(sm)  # Calls sm.update(msg)

    def __init__(self):
        """
        Do not create instances of this class! Statemachines is a singleton.
        """
        super().__init__(daemon=True)
        self.statemachines_dict = {}  # {MsgType1: [sm1, sm2], MsgType2: [sm33], ...}
        self.worker_queue = Queue()  # Queue of statemachines to be updated.
        self.worker_queue_max_size = 2  # When the queue exceeds this size a new Worker will be created.
        self.workers = [Statemachines.Worker(self.worker_queue)]  # list of workers
        self.message_queue = Queue()  # New published messages by an Actor shall be pushed to this queue.
        self.start()

    @staticmethod
    def get_instance():
        """
         The Statemachines class is a singleton and should only be accessed through this function.

         Example:
             statemachines = Statemachines.get_instance()

         :return: an instance of the Statemachines class.
         """
        if Statemachines.__instance__ is None:
            Statemachines.__instance__ = Statemachines()
        return Statemachines.__instance__

    def run(self):
        while True:
            msg = self.message_queue.get()
            if msg is not None:
                statemachine_list = self.statemachines_dict.get(type(msg))
                if statemachine_list is not None:
                    for statemachine in statemachine_list:
                        self.worker_queue.put((lambda sm: sm.update(msg), statemachine))
                        if self.worker_queue.qsize() > self.worker_queue_max_size:
                            self.workers.append(Statemachines.Worker(self.worker_queue))
                            self.worker_queue_max_size *= 2

    def register(self, statemachine: Statemachine):
        """
         Registers a statemachine.

         Example:
             Statemachines.get_instance().register(statemachine)
         """
        if statemachine is not None:
            for state in statemachine.states:
                for trans in state.transitions:
                    if trans.trans_type == TransitionType.MESSAGE:
                        message_trans = cast(MessageTrans, trans)
                        statemachine_list = self.statemachines_dict.get(message_trans.msg_type)
                        if statemachine_list is None:
                            statemachine_list = [statemachine]
                        elif statemachine not in statemachine_list:
                            statemachine_list.append(statemachine)
                        self.statemachines_dict[message_trans.msg_type] = statemachine_list
