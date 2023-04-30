# Reactive systems using Actors
Dear all,

Welcome to a C++/Python library for creating reactive systems based on the Actors model.

## Idea
The idea with this library is to create a framework for creating highly performant, scalable and maintainable code. My inspiration for this project originates from the following sources:

* Actors Model (https://en.wikipedia.org/wiki/Actor_model)
* ROS (https://www.ros.org)
* RxROS (https://github.com/rosin-project/rxros)
* RxROS2 (https://github.com/rosin-project/rxros2)
* Reactive Programming (https://reactivex.io)
* Reactive systems (https://www.reactivemanifesto.org)

Although all the references to ROS, the library has as such nothing to do with programming robots. It is a general purpose library/framework for creating reactive systems.

## Approach
Throughout my career I have always found the following item central for producing high quality software

* Low coupling/high cohesion<br>Low coupling/high cohesion is a central part of the Actors model and therefore also a central part of this library. The only way Actors can communicate with each other is through messages. An actor can publish a message and scribe and react to published messages. Each and every actor lives it own life. It will newer break due to major changes in other Actors. The developer can concentrate on developing the best Actor in the wold without ever having to think of how other Actors are implemented. An Actor may start other actors to perform its task. This is high cohesion. The only dependency between Actors are the messages and the properties/data they carries – so designing a system based on Actors is all about creating proper messages that can be distributed and processed by other Actors.
* Reusability<br>Reusability of code is the use of existing software, or software knowledge,Actors to build new software (ref. https://en.wikipedia.org/wiki/Code_reuse). This is of course the fundamental idea with library. I just hope the library has the quality that is needed to be used over and over again in many projects.
* Keep it simple<br>Keep it simple! Well, well, well - I could talk hours about this subject, but this is not the purpose of this project. I think you know what I am talking about, especially if you have tried to take over the maintenance of the code your "dear" colleague produced just before he left the company. Even code that I produced myself is hard to read and understand after having been away from it for say ½ a year. I have put a lot of work in make this code easy to read and understand, but it is in the usage of the library that the "keep it simple" statement really should shine through.

It is my hope that the above items are reflected in the code and especially the usage it.  

### Project phases
This library is a work in progress, and it will continue to be so probably for many years, but I forsee at least two phases for the library. Phase1 is related to only adding features to the library. This includes:

* Logging<br>Logging is one of the most fundamental debuging facitilities a library shall provide. It shall be easy to enable and use. A log entry shall contain a time stamp, severity, which Actor created the entry and a text that describes a problem or essentail information about the state of the Actor.
* Http<br>A Web page shall be available for each Actor. The purpose of the web page is to provide monitoring of an Actor. More advanced web pages that collects information on the overall application (Actors), will be added later.
* Statistics<br>Statistics is like logging essential for debugging your program. It shall be possible to see how many messages of a given type have been published and how long time has gone sine we received the last message. Queue sizes and number of worker threads should also be information that easily can be shown. All these information could in principle be shown in a web page. Will be decided at a later time.
* Scheduling and Timers<br>Scheduling and timer are fundamental of all systems and shall as such be part of this library.
* State machines<br>State machines are part of nearly all systems. However, they come in many variants/implementations and it is always complicated to understand how they work and what they do. A new approach to state machines will be presented in this library. The implementation will be very close to the definition of a state machine.
* Behavir trees<br>Experimental feature that will be added to the library.
* Reactive programming<br>Experiment feature that will be added to the library. Insrted of looking at a system that is based on messages that is passed from on Actor to anothor, we could also look at it as system of message streams that. When we take take that view 

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase1.png" height="400"><br>
  Phase1: Focus is to provide different features for Actors.
</p>

The second phase is only related to create a distributed system of Actors that can communicate with each other on multiple platforms and hosts.

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase2.png" height="400"><br>
  Phase2: Focus is to provide a distributed environment for sharing messages between Actors.
</p>

Now you may think why all the fuss about logging, scheduler and timers. All programming languages provides these facilities either directly or as libraries that easily can be included. My answer to this falls back to "the keep it simple" item. The programmer should be presented with a homogen and coherent interface that supports many of task that are required to build a system. What then about configuration, network access, database access etc.? 



## Installation and Setup
The Actors library is dependand on the ReactiveX extensions RxPY (see https://github.com/ReactiveX/RxPY) and RxCpp (see https://github.com/ReactiveX/RxCpp). These two extensions must therefore be installed prior to installing the Actors library. The insrallation process is as follows:

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
make install 
```

### Installation of the Actors library on Linux

```bash
git clone https://github.com/henrik7264/Actors.git
```

#### Testing the Python Actors library on Linux

```bash
cd Actors/py_actors
export PYTHONPATH=`pwd`
python3 example_publisher_subscriber/main.py
python3 example_statemachine/main2.py
```

