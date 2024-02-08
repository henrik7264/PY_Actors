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

import inspect
from typing import cast
from enum import Enum
from threading import Lock
from lib_actors.dispatcher import Dispatcher
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

    def __init__(self, transition_type: TransitionType, action=None, next_state=None):
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
                                 Message(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 Message(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 Timer(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param transition_type: The type of the transition, either a Message or Timer.
        :param action: A callback function that is executed each time a transition is triggered.
        :param next_state: The next state of the statemachine. Set as part of a transition is triggered.
        """

        self.transition_type = transition_type
        self.action = action
        self.next_state = next_state
        self.statemachine = None

    def set_statemachine(self, statemachine):
        """
        Internal function - do not use!

        Sets the statemachine, so the current state of statemachine can be updated as part of a transition.

        :param statemachine: A Statemachine.
        :return:
        """
        self.statemachine = statemachine


class Message(Transition):
    """
    A Message is a transition that is triggered by a message published by an Actor.
    """

    def __init__(self, msg_type, action=None, next_state=None):
        """
        A Message is a transition that is triggered by a message published by an Actor.

        The Message must specify the exact message type that triggers the transition.
        It must also specify an action which is a callback function that called each time the transition is triggered.
        Finally, it must specify a next state which the statemachine will be in the transition is complete.

        Example:
            Message(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED),

        :param msg_type: The specific message type that will trigger the transition.
        :param action: A callback function that is executed when the transition is triggered.
        :param next_state: The next state of the statemachine when then transition is complete.
        """
        super().__init__(transition_type=TransitionType.MESSAGE, action=action, next_state=next_state)
        self.msg_type = msg_type

    def do_action(self, msg):
        """
        Internal function - do not use!
        Actual execution of the action callback function of the transition.

        :param msg: A message published by an Actor.
        """
        curr_state = self.statemachine.current_state
        with self.statemachine.transition_lock:
            if curr_state == self.statemachine.current_state:
                if self.action is not None:
                    with self.statemachine.actor_lock:
                        self.action(msg)
                if self.next_state is not None:
                    self.statemachine.set_current_state(self.next_state)


class Timer(Transition):
    """
    A Timer is a transition that is triggered by a timer when it times out.
    """

    def __init__(self, timeout: int, action=None, next_state=None):
        """
        A Timer is a transition that is triggered by a timer when it times out.

        The Timer must specify the timeout of the timer.
        It must also specify an action which is a callback function that called when the timer times out.
        Finally, it must specify a next state which the statemachine will be in the transition is complete.

        Example:
            Timer(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED),

        :param timeout: The timeout in milliseconds. When the timer times out the transition will be triggered.
        :param action: A callback function that is executed when the transition is triggered.
        :param next_state: The next state of the statemachine when then transition is complete.
        """

        super().__init__(transition_type=TransitionType.TIMER, action=action, next_state=next_state)
        self.timeout = timeout

    def do_action(self):
        """
        Internal function - do not use!
        Actual execution of the action callback function of the transition.
        """
        curr_state = self.statemachine.current_state
        with self.statemachine.transition_lock:
            if curr_state == self.statemachine.current_state:
                if self.action is not None:
                    with self.statemachine.actor_lock:
                        self.action()
                if self.next_state is not None:
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
                                 Message(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 Message(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 Timer(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param state_name: The name of a State, typically an enum, i.e. integer.
        :param transitions: A number of transitions that when triggered will change the state of the statemachine.
        """
        self.state_name = state_name  # typically an enum, i.e. integer
        self.transitions = transitions  # The transitions of a state
        self.message_list = []  # [(MsgType1 Trans1), (MsgType2: Trans2), ...}
        self.timers_list = []  # [Trans3, Trans4 ...]
        for trans in self.transitions:
            if trans.transition_type == TransitionType.MESSAGE:
                message = cast(Message, trans)
                self.message_list.append((message, message.msg_type))
            elif trans.transition_type == TransitionType.TIMER:
                timer = cast(Timer, trans)
                self.timers_list.append(timer)

    def set_statemachine(self, statemachine):
        """
        Internal function - do not use!

        Forwards the statemachine instance to all transitions.

        :param statemachine: A Statemachine.
        """
        for trans in self.transitions:
            trans.set_statemachine(statemachine)


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

    def __init__(self, initial_state, *states: State):
        """
        A statemachine is defined by an initial state and a number of states it can change to at any given time

        Example:
            class States(Enum):
                DOOR_OPENED = 0,
                DOOR_CLOSED = 1
            self.sm = Statemachine(States.DOOR_CLOSED,
                           State(States.DOOR_CLOSED,
                                 Message(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                           State(States.DOOR_OPENED,
                                 Message(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                                 Timer(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

        :param initial_state: The initial state of the Statemachine
        :param states: A number of states of the statemachine.
        """
        actor = inspect.currentframe().f_back.f_locals["self"]  # Dirty trick to get the Actor instance.
        assert hasattr(actor, "lock")
        self.actor_lock = actor.lock  # Lock from Actor to synchronize callback functions.
        self.transition_lock = Lock()
        self.statemachine_lock = Lock()  # Lock to ensure statemachine synchronization.
        self.current_state = None  # Current state of the Statemachine, typically an enum, i.e. integer
        self.states = states  # The states of a statemachine
        self.state_dict = {}  # { name1: State1, name2: State2, ...}, name is typically an enum, i.e. integer
        self.scheduler = Scheduler.get_instance()
        self.dispatcher = Dispatcher.get_instance()
        self.jobs = []  # [job_id1, job_id2, ...]
        self.subscriptions = []  # [(sub_id1, msg_type1), (sub_id2, msg_type2) ...]
        for state in self.states:
            state.set_statemachine(self)
            self.state_dict[state.state_name] = state
        self.set_current_state(initial_state)

    def get_current_state(self):
        """
        Returns the current state of a statemachine.

        Example:
            self.curr_state = self.statemachine.get_current_state()

        :return: Current state of the statemachine. Typically, an enum or integer.
        """
        with self.statemachine_lock:
            return self.current_state

    def set_current_state(self, new_state):
        """
        Internal function - do not use!

        The function sets the current state of the statemachine.
        Only a Transition should set the current state of the statemachine.

        :param new_state: The new/current state of the statemachine.
        """
        with self.statemachine_lock:
            for job_id in self.jobs:
                self.scheduler.remove(job_id)
            self.jobs = []
            for (sub_id, msg_type) in self.subscriptions:
                self.dispatcher.unregister_cb(sub_id, msg_type)
            self.subscriptions = []

            if new_state is not None:
                self.current_state = new_state

            state = self.state_dict.get(self.current_state)
            if state is not None:
                for timer in state.timers_list:
                    job_id = self.scheduler.once(timer.timeout, timer.do_action)
                    self.jobs.append(job_id)
                for (message, msg_type) in state.message_list:
                    sub_id = self.dispatcher.register_cb(message.do_action, msg_type)
                    self.subscriptions.append((sub_id, msg_type))
