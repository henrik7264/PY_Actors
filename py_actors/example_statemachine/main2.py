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

import time
from example_statemachine.publish_actor import Publisher
from example_statemachine.smachine_actor import SMachine

if __name__ == "__main__":
    # Initialize actors
    actors = [Publisher(), SMachine()]

    # Let the program run for 10 sec.
    time.sleep(10.0)
    print(actors[0].count)
    print(actors[1].count)
    exit(0)