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
from enum import Enum
from lib_actors.actor import Actor
from lib_actors.statemachine import Statemachine, State, MessageTrans, TimerTrans
from example_statemachine.messages import OpenDoorMsg, CloseDoorMsg


class SMachine(Actor):
    def __init__(self):
        super().__init__("Statemachine", logging.NOTSET)
        self.count = 0

        class States(Enum):
            DOOR_OPENED = 0,
            DOOR_CLOSED = 1
        self.sm = Statemachine(self, States.DOOR_CLOSED,
                       State(States.DOOR_CLOSED,
                             MessageTrans(OpenDoorMsg, action=self.open_door, next_state=States.DOOR_OPENED)),
                       State(States.DOOR_OPENED,
                             MessageTrans(CloseDoorMsg, action=self.close_door, next_state=States.DOOR_CLOSED),
                             TimerTrans(1000, action=self.auto_close_door, next_state=States.DOOR_CLOSED)))

    def open_door(self, msg: OpenDoorMsg):
        self.logger.info("Opening door in state " + str(self.sm.get_current_state()))
        self.count += 1

    def close_door(self, msg: CloseDoorMsg):
        self.logger.info("Closing door in state " + str(self.sm.get_current_state()))
        self.count += 1

    def auto_close_door(self):
        self.logger.info("Auto Closing door in state " + str(self.sm.get_current_state()))
