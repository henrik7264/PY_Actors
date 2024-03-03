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
from example_publisher_subscriber_nodes.message import Message
from lib_actors.node import Node


class Publisher(Node):
    def __init__(self):
        super().__init__('Publisher', 'localhost', 5678, send_msgs=[Message])
        self.node.add_peer('Subscriber', 'localhost', 8765)

        self.count = 0
        self.scheduler.repeat(1000, self.pub)

    def pub(self):
        self.message.publish(Message("Hello " + str(self.count)))
        self.count += 1


if __name__ == "__main__":
    publisher = Publisher()

    time.sleep(10.0)
    exit(0)
