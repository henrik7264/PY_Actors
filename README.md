# Reactive Systems using Actors
Dear all,

Welcome to ReSyAct a C++/Python library for creating Reactive Systems based on the Actors model.

Be aware that the library currently is a work in progress and may change without any notice. An early version of the Python library is available. It's a proof of concept version that provides the basic Actors functionality and most of the features discussed below. The C++ version will soon be ready and added to the repository with the same set of features. The library have been tested informally on a
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
* Keep it simple<br>Keep it simple! Well, well, well - I could talk hours about this subject, but this is not the purpose of this section. I think you know what I am talking about, especially if you have tried to take over the maintenance of some code your "dear" colleague produced just before he left the company. Even code that I produced myself is hard to read and understand after having been away from it for say ½ a year. I have put a lot of work in make this code easy to read and understand, but it is in the usage of the library that the "keep it simple" statement really should shine through.

It is my hope that the above items are reflected in the code and especially the usage it, and that the library provides a solid foundation for creating reactive systems based on Actors.

### Project phases
I foresee at least two phases for the library. Phase1 is related to only adding features to the library. This includes:

* Logging<br>Logging is one of the most fundamental debugging facilities a library like this must provide. It shall be easy to enable and use. A log entry shall contain a time stamp, severity, which Actor created the entry and a text that describes a problem or information about the state of the Actor.
* Http<br>A Web page shall be available for each Actor. The purpose of the web page is to provide monitoring of an Actor. More advanced web pages that collects information on the overall application (Actors), will be added later.
* Statistics<br>Statistics is like logging essential for debugging a program. It shall be possible to see how many messages of a given type have been published and how long time has gone sine we received the last message. Queue sizes and number of worker threads should also be information that easily can be shown. All these information could in principle be shown in a web page. This Will be decided at a later time.
* Scheduling and Timers<br>Scheduling and timers are fundamental of all systems and shall as such be part of this library.
* State machines<br>State machines are part of nearly all systems. However, they come in many variants/implementations and it is always complicated to understand how they work and what they do. A simple approach to state machines will be presented in this library. The implementation will be very close to the definition of a state machine.
* Behavior trees<br>Experimental feature that will be added to the library.
* Reactive programming<br>Experimental feature that will be added to the library. Instead of looking at a system that is based on parsning messages from one Actor to anothor, we could also look at it as system of message streams that are processed by the Actors. When we take that view reactive programming becomes a natural way of processing the messages. See some of the advantages of using reactive programming on ttps://reactivex.io - they are awasome.

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
The ReSyAct library depends on the following software:

* Python3 (Seen it run on a Python v3.6)
* C++ compiler suporting v17.
* RxPY v4 (see https://github.com/ReactiveX/RxPY)
* RxCPP v? (see https://github.com/ReactiveX/RxCpp)

## Installation and setup
The ReSyAct library depends on the ReactiveX extensions RxPY and RxCpp. These two extensions must be installed prior to installing the library. The installation process is as follows:

1. Install RxPy
2. Install RxCPP
3. Install ReSyAct library

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

### Installation of the ReSyAct library on Linux

```bash
git clone https://github.com/henrik7264/ReSyAct.git
```

#### Testing the Python library on Linux

```bash
cd ReSyAct/py_actors
export PYTHONPATH=`pwd`
python3 example_publisher_subscriber/main.py
python3 example_statemachine/main2.py
```

## Using the ReSyAct library in your own project.
OK, now to the more fun part of using the ReSyAct library. The following sections describe messages, actors, schedulers, timers and state machies. As the library expands new features will be added.

### Messages (Python)
Messages is one of the most important concepts of the ReSyAct library. A message is simply a class!

The most simple message consist of nothing more than a class definition:

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
There are two operations which can be applied on messages: That is to subscribe to a message and to publish a message.

#### Subscribe to a Message
The Actor will subscribe to the specified message type and call the callback function each time a message of the specified type is published.

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

The sequence diagram below show how the subscription and publish of messages work. The Actor starts by subscribing to a number of messages (message types). A callback function is associated to each subscription. 

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Publish_Subscribe.png"><br>
  Sequence diagram showing the subscribe and publish mechanism of the ReSyAct Library.
</p>

Each time a message is published by an Actor the set of callback functions that have subscribed to the message will be executed. This takes place in the Dispatcher where a number of Worker threads will take care of the execution. The published message reach the 

There are some problems related to this architecture:
1. While executing one callback function another message may be published and trigger another callback function. This could in worse case lead to thread synchronization problems. The ReSyAct library solves this problem by allowing only one callback function per Actor to execute at a time, i.e. 100 Actors can concurrently execute 100 callback functions, but one Actor can only execute one callback function at a time.
2. A heavy message load may create the situation described in item 1. To accommodate for this problem the ReSyAct library will adapt the number of Workers to the message load, i.e. another Worker will be added to the Dispatcher if the messages cannot be handled as fast as they arrive. This can in worse case lead to a large amount Workers (threads).

### Actors (Python)
Actors is like messages a central part of the ReSyAct library. All Actors are sub-classes of an Actor class 

#### Creation of an Actor
```python
class MyActor(Actor):
        def __init__(self):
            super().__init__("MyActor", logging.NOTSET)
```

It is as simple as that! The Actor takes as argument the name of the Actor. It must be a unique name that is easy to identify in ex. log message. The second argument is the log level. The default log level is set to CRITICAL. Set it to logging.NOTSET to log everything.

Initialization of an Actor simply consist of creating an instance of it. It can be done anywhere and at any time. The Actor instance must exists throughout the lifetime of the application.

```python
if __name__ == "__main__":
    # Initialize actors
    actors = [MyActor(), AnotherActor(), AThirdActor()]
    ...
```

An Actor is a facade to message handling, scheduling, logging etc. As soon we are in the scope of an Actor all the functions will be available. This includes:

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

self.tmer = Timer(...)
self.sm = Statemachine(...)

Observe how the functions are organized into logical groups - this makes it very easy to understand and use. Only Timer and Statemachine 

### Logging (Python)

### Schedulers (Python)

### Timers (Python)

### State Machines (Python)

### Message Streams (Python)
