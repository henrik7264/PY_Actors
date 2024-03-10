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

import time
import logging
from example_publisher_subscriber_nodes.message import Message
from lib_actors.node import Node


class Subscriber(Node):
    def __init__(self):
        super().__init__('Subscriber', 'localhost', 8765, [Message])
        self.logger.setLevel(logging.NOTSET)

        self.count = 0
        self.message.subscribe(self.sub, Message)

    def sub(self, msg: Message):
        self.logger.info(msg.data)
        self.count += 1


if __name__ == "__main__":
    sub = Subscriber()

    time.sleep(10.0)
    exit(0)
