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


class Node2(Node):
    def __init__(self):
        super().__init__('Node2', 'localhost', 8765, [Msg1, Msg2, Msg3, Msg4])
        self.node.add_peer('Node1', 'localhost', 5678)
        self.node.add_peer('Node3', 'localhost', 6789)
        self.logger.setLevel(logging.NOTSET)

        self.count = 0
        self.scheduler.repeat(1000, self.pub)
        self.message.subscribe(self.sub1, Msg1)
        self.message.subscribe(self.sub3, Msg3)

    def pub(self):
        rnd = random()
        if rnd < 0.25:
            self.logger.info("Sending Msg2 ...")
            self.message.publish(Msg2())
        elif rnd < 0.5:
            self.logger.info("Sending Msg4 ...")
            self.message.publish(Msg4())
        self.count += 1

    def sub1(self, msg: Msg1):
        self.logger.info("Received Msg1 ...")

    def sub3(self, msg: Msg3):
        self.logger.info("Received Msg3 ...")


if __name__ == "__main__":
    node2 = Node2()

    time.sleep(1000.0)
    exit(0)
