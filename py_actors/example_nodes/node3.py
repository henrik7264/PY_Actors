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
import time
from random import random
from lib_actors.node import Node
from example_nodes.messages import *


class Node3(Node):
    def __init__(self):
        super().__init__('Node3', 'localhost', 6789, [Msg3, Msg4])
        self.node.add_peer('Node2', 'localhost', 8765)
        self.logger.setLevel(logging.NOTSET)

        self.count = 0
        self.scheduler.repeat(1000, self.pub)
        self.message.subscribe(self.sub3, Msg3)
        self.message.subscribe(self.sub4, Msg4)

    def pub(self):
        rnd = random()
        if rnd < 0.25:
            self.logger.info("Sending Msg3 ...")
            self.message.publish(Msg3())
        if rnd < 0.5:
            self.logger.info("Sending Msg4 ...")
            self.message.publish(Msg4())
        self.count += 1

    def sub3(self, msg: Msg3):
        self.logger.info("Received Msg3 ...")

    def sub4(self, msg: Msg4):
        self.logger.info("Received Msg4 ...")


if __name__ == "__main__":
    node3 = Node3()

    time.sleep(1000.0)
    exit(0)
