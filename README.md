# Reactive Systems using Actors
Dear all,

Welcome to Actors - a C++/Python library for creating Reactive Systems based on the Actors model.

Be aware that the library currently is a work in progress and may change without any notice. An early version of the Python library is available. It's a proof of concept version that provides the basic Actors functionality and most of the features discussed below. The C++ version will soon be ready and added to the repository with the same set of features. The library has been tested informally on a
* Beaglebone Black (Debian 10.3, Python v3.6)
* Raspberry Pi 4 (Ubuntu 20,04 server)
* Portable PC (i7-9750H CPU, Ubuntu 22.04, Python v3.10, g++ v11.3) 
* High end PC (i9-12900k CPU, Fedora 37, Python v3.11, g++ v12.2)

## Idea
The idea with this library is to create a framework for creating highly performant, scalable and maintainable code. My inspiration for this project originates from the following sources:

* Actors Model (https://en.wikipedia.org/wiki/Actor_model)
* ROS (https://www.ros.org)
* RxROS (https://github.com/rosin-project/rxros)
* RxROS2 (https://github.com/rosin-project/rxros2)
* Reactive Programming (https://reactivex.io)
* Reactive systems (https://www.reactivemanifesto.org)

Although there are several references to ROS, the library has as such nothing to do with programming robots. It is a general purpose library/framework for creating reactive systems.

## Approach
I have always found the following items central for producing high quality software

* Low coupling/high cohesion<br>Low coupling/high cohesion is a central part of the Actors model and therefore also a central part of this library. The only way Actors can communicate with each other is through messages. An actor can publish a message and scribe and react to published messages. Each and every actor lives it own life. It will newer break due to major changes in other Actors. The developer can concentrate on developing the best Actor in the wold without ever having to think of how other Actors are implemented. An Actor may start other actors to perform its task. The only dependency between Actors are the messages and the properties/data they carries – so designing a system based on Actors is all about creating proper messages that can be distributed and processed by other Actors.
* Reusability<br>Reusability of code is the use of existing software, or software knowledge, to build new software (ref. https://en.wikipedia.org/wiki/Code_reuse). This is of course the fundamental idea with library. I just hope the library has the quality that is needed to be used over and over again in many projects.
* Keep it simple<br>Keep it simple! Well, well, well - I could talk hours about this subject, but this is not the purpose of this section. I think you know what I am talking about, especially if you have tried to take over the maintenance of some code your "dear" colleague produced just before he left the company. Even code that I produced myself is hard to read and understand after having been away from it for say ½ a year. I have put a lot of work in making this code easy to read and understand, but it is in the usage of the library that the "keep it simple" statement really should shine through.

It is my hope that the above items are reflected in the code and especially the usage it, and that the library provides a solid foundation for creating reactive systems based on Actors.

### Project phases
I foresee at least two phases for the library. Phase1 is related to only adding features to the library. This includes:

* Logging<br>Logging is one of the most fundamental debugging facilities a library like this must provide. It shall be easy to enable and use. A log entry shall contain a time stamp, severity, which Actor created the entry and a text that describes a problem or information about the state of the Actor.
* Http<br>A Web page shall be available for each Actor. The purpose of the web page is to provide monitoring of an Actor. More advanced web pages that collects information on the overall application (Actors), will be added later.
* Statistics<br>Statistics is like logging essential for debugging a program. It shall be possible to see how many messages of a given type have been published and how long time has gone sine we received the last message. Queue sizes and number of worker threads should also be information that easily can be shown. All these information could in principle be shown in a web page. This Will be decided at a later time.
* Scheduling and Timers<br>Scheduling and timers are fundamental of all systems and shall as such be part of this library.
* State machines<br>State machines are part of nearly all systems. However, they come in many variants/implementations and it is always complicated to understand how they work and what they do. A simple approach to state machines will be presented in this library. The implementation will be very close to the definition of a state machine.
* Behavior trees<br>Experimental feature that will be added to the library.
* Reactive programming<br>Experimental feature that will be added to the library. Instead of looking at a system that is based on parsing messages from one Actor to anothor, we could also look at it as system of message streams that are processed by the Actors. When we take this view reactive programming becomes a natural way of processing the messages. See some of the advantages of using reactive programming on ttps://reactivex.io - they are awasome.

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase1.png" height="400"><br>
  Phase1: Focus is to provide different features for Actors.
</p>

The second phase is only related to create a distributed system of Actors that can communicate with each other on multiple platforms and hosts.

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase2.png" height="400"><br>
  Phase2: Focus is to provide a distributed environment for sharing messages between Actors.
</p>

The progress of this library depends a lot on the interest for it and if the overall goals actually are met.

## Required software
The Actors library depends on the following software:

* Python3 (Seen it run on a Python v3.6)
* C++ compiler suporting v17.
* RxPY v4 (see https://github.com/ReactiveX/RxPY)
* RxCPP v? (see https://github.com/ReactiveX/RxCpp)

## Installation and setup
The Actors library depends on the ReactiveX extensions RxPY and RxCpp. These two extensions must be installed prior to installing the library. The installation process is as follows:

1. Install RxPy
2. Install RxCPP
3. Install Actors library

### Installation of RxPY on Linux

```bash
pip3 install reactivex
```

### Installation of RxCPP on Linux

```bash
git clone --recursive https://github.com/ReactiveX/RxCpp.git
cd RxCpp
mkdir build
cd build
cmake ..
sudo make install 
```

### Installation of the Actors library on Linux

```bash
git clone https://github.com/henrik7264/Actors.git
```

#### Testing the Python library on Linux

```bash
cd Actors/py_actors
export PYTHONPATH=`pwd`
python3 example_publisher_subscriber/main.py
python3 example_statemachine/main2.py
```

## Using the Actors library in your own project.
Now to the more fun part of using the Actors library. 

### Project setup (Python)
There is currently no installation packages for the Actors library. The code is simply indented to be included directly in your project. Copy the lib_actors folder directly into your project and start to create new actors as described below:

```bash
YouProject/
  lib_actors/
  ...
  actor1/
  actor2/
  ...
  main.py
```

A number of examples are provided as part of the Actors library. They should provide enough information to setup your development environment.

## Features of the Actor library
The following sections describe messages, actors, schedulers, timers and state machines. As the library expands new features will be added

### Messages (Python)
Messages are one of the most important concepts of the Actors library. A message is simply a class!

The most simple message consist of nothing but a class definition:

```python
class SimpleMsg:
  pass
```

Messages may carry data and even functions that can be executed when a message is received:

```python
class MyMessage:
    def __init__(self, name: str, count: int):
        self.name: str = name
        self.count: int = count
```

#### Operations on messages (Python)
There are two operations which can be applied on messages: This is to subscribe to a message and to publish a message.

#### Subscribe to a Message
An Actor will subscribe to a specific message type by providing a callback function that is executed each time a message of that type is published.

##### Syntax 
```python
def subscribe(self, msg_type, func) -> None:

# msg_type: A reference to a class/message.
# func: A lambda or callback function. The function must take a message argument of the specified type.
```

##### Example
```python
self.message.subscribe(MyMessage, self.func)

def func(self, msg: MyMessage):
  self.logger.debug("Received a MyMessage: " + msg.name + ", " + str(msg.count))
```

#### Publish a Message
The Actor will publish the specified message. 

##### Syntax
```python
def publish(self, msg) -> None:

# msg: The message (instance of a class) to be published.
```

##### Example
```python
self.message.publish(MyMessage("Hello world", 1234))
```

The sequence diagram below shows how the subscription and publishing of messages work. The Actor starts by subscribing to a number of messages (message types). A callback function is associated to each subscription. Each time a message is published the set of callback functions that have subscribed to the message will be executed. This takes place in the Dispatcher where a number of Worker threads will take care of the execution.

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Publish_Subscribe.png"><br>
  Sequence diagram showing the subscribe and publish mechanism of the Actors Library.
</p>

There are some problems related to this execution model/architecture:
1. While executing one callback function another message may be published and trigger another callback function. This could in worse case lead to thread synchronization problems. The Actors library solves this problem by allowing only one callback function per Actor to execute at a time, i.e. 100 Actors can concurrently execute 100 callback functions, but one Actor can only execute one callback function at a time.
2. A heavy message load may create the situation described in item 1. To accommodate for this problem, the Actors library will adapt the number of Workers to the message load, i.e. another Worker will be added to the Dispatcher if the messages cannot be handled as fast as they arrive. This can in worse case lead to a large amount Workers (threads).

The problems described above are common for this kind of architecture. There is no real solution to the problem except that the architect and programmer must ensure that the hardware platform is dimentioned to the message load of the system and that the callback functions are fast and responsive. Avoid sleep, wait and I/O operations in callback functions that are called often.

### Actors (Python)
Actors are, like messages, a central part of the Actors library. All Actors are sub-classes of an Actor class 

#### Creation of an Actor
```python
class MyActor(Actor):
        def __init__(self):
            super().__init__("MyActor", logging.NOTSET)
```

It is as simple as that! The Actor takes as argument the name of the Actor. It must be a unique name that is easy to identify in ex. log message. The second argument is the log level. The default log level is set to CRITICAL. Set it to logging.NOTSET to log everything.

Initialization of an Actor consist of creating an instance of it. It can be done from anywhere and at any time - Even an Actor may create new Actors. The instance of an Actor must exists throughout the lifetime of the application. 

```python
if __name__ == "__main__":
    # Initialize actors
    actors = [MyActor(), ASecondActor(), AThirdActor()]
    ...
```

An Actor is implemented as a facade. As soon we are in the scope of an Actor a set of functions becomes available. This includes:

```python
self.message.subscribe(...)
self.message.publish(...)
self.message.stream(...)

self.logger.debug(...)
self.logger.info(...)
self.logger.warning(...)
self.logger.error(...)
self.logger.critical(...)

self.scheduler.once(...)
self.scheduler.repeat(...)
self.scheduler.remove(...)

self.timer = Timer(...)
self.sm = Statemachine(...)
```

Observe how the functions are organized into logical groups. This makes it very easy to understand and use them. Only Timer and Statemachine are a bit different due to their usage/nature. 

### Logging (Python)
The logging interface of the Actors library is based on the Python logging library. The Python library has been slightly adapted so that the name of the Actor is included in the log message. Default is to log to a terminal and a file named "actors.log", and the log level is set to CRITICAL. The log level can be changed during creation of the Actor. In fact, all features of the Python logging library are available and can be changed if needed. It is however recommended to use the following interface to log messages:

#### Interface
```python
self.logger.debug(msg, *args, **kwargs)
self.logger.info(msg, *args, **kwargs)
self.logger.warning(msg, *args, **kwargs)
self.logger.error(msg, *args, **kwargs)
self.logger.critical(msg, *args, **kwargs)
```
The msg is the message format string, and the args are the arguments which are merged into msg using the string formatting operator (source https://docs.python.org/3/library/logging.html).

### Example
```python
self.logger.info("Received a MyMessage: " + msg.name + ", " + str(msg.count))
```

The code will produce the following log entry:
```
2023-01-01 23:19:49,175 MyActor INFO: Received a MyMessage: Hello World, 1234
```

### Scheduler (Python)
A Scheduler is a timing mechanism. It can be used to execute a task (function call) at a given time. The task can be executed once or repeated until it is removed. The scheduled tasks are executed by an adaptable number of Workers. If the Workers are not able to execute the tasks as requested by the secheduler additional Workers will be started to execute the tasks. This situaltion happens when many tasks are scheduled at the same time. The situation is not different from handling messages (see above section) - in fact it is exctaly the same and the Actors library will behave the same way:

1. While executing one task/callback function another task may be triggered by a scheduler timeout or a published message. This could in worse case lead to thread synchronization problems. The Actors library solves this problem by allowing only one task/callback function per Actor to execute at a time, i.e. 100 Actors can concurrently execute 100 tasks/callback functions, but one Actor can only execute one callback function at a time.
2. A heavy message or scheduler load may create the situation described in item 1. To accommodate for this problem, the Actors library will adapt the number of Workers , i.e. another Worker will be added to the Dispatcher/Scheduler if the messages cannot be handled as fast as they arrive. This can in worse case lead to a large amount Workers (threads).

Again, the Actors library will do what it can to solve the problem, but the root cause of the problem is a insufficient hardware platform and/or poor implementations of the tasts/callback functions. It is in these two areas the problem should be resolved.

The scheduler interface is defined as follows:

#### Schedule a task once
A task can be executed once at a given time by the Scheduler.  It is possible to to cancel/remove the canceled time

##### Syntax 
```python
def once(self, msec: int, func) -> int:

# msec: timeout in milliseconds.
# func: call back function to be executed when the job times out.
# return: job_id
```

##### Example
```python
job_id = self.scheduler.once(1000, self.func)

def func(self):
  self.logger.debug("The scheduled job timedout.")
```

### Timers (Python)

### State Machines (Python)

### Message Streams (Python)
