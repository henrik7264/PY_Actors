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
from lib_actors.actor import Actor
from example_publisher_subscriber.message import Message


class Subscriber(Actor):
    def __init__(self):
        super().__init__("Subscriber", logging.NOTSET)
        self.count = 0
        self.message.subscribe(Message, self.sub)

    def sub(self, msg: Message):
        self.logger.info(msg.data)
        self.count += 1
