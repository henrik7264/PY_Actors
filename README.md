# Actors
Dear all,

Welcome to an Actors library for C++/Python. You will very soon realize that this is much more that just a library for creating Actors - my hope with this project is to create a framework for creating spectacular software systems.

## Idea
The idea with this library is to create a framework for creating highly performant, scalable and maintainable code. My inspiration for this project originates from the following sources:

* Actors Model (https://en.wikipedia.org/wiki/Actor_model)
* ROS (https://www.ros.org)
* RxROS (https://github.com/rosin-project/rxros)
* RxROS2 (https://github.com/rosin-project/rxros2)
* Reactive Programming (https://reactivex.io)
* Reactive systems (https://www.reactivemanifesto.org)

Although all the references to ROS, the Actors library has as such nothing to do with programming robots. It is a general purpose library/framework for creating reactive systems.

## Approach
Throughout my career as a software developer I have always found the following item central for producing high quality software

* Low coupling/high cohesion
* Reusability
* Keep it simple

Low coupling/high cohesion is a central part of the Actors model and therefore also a central part of this library. The only way Actors can communicate with each other is through messages. An actor can publish a message and scribe and react to published messages. Each and every actor lives it own life. It will newer break due to major changes in other Actors. The developer can concentrate on developing the best Actor in the wold without ever having to think of how other Actors are implemented. An Actor may start other actors to perform its task. This is high cohesion. The only dependency between Actors are the messages and the properties/data they carries – so designing a system based on Actors is all about creating proper messages that can be distributed and processed by other Actors.

Reusability of code is the use of existing software, or software knowledge, to build new software (ref. https://en.wikipedia.org/wiki/Code_reuse). This is of course the fundamental idea with library. I just hope the library has the quality that is needed to be used over and over again in many projects.

Keep it simple! Well, well, well - I could talk hours about this subject, but this is not the purpose of this project. I think you know what I am talking about, especially if you have tried to take over the maintenance of the code your "dear" colleague produced just before he left the company. Even code that I produced myself is hard to read and understand after having been away from it for say ½ a year. I have put a lot of work in make this code easy to read and understand, but it is in the usage of the library that the "keep it simple" statement really should shine through.

### Project phases

The project is split in two phases. Phase1 is related to only adding features to the library. This includes:
* Logging.<br>Logging is one of the most fundamental debuging facitilities a library shall provide. It shall be easy to enable and use. A log entry shall contain a time stamp, severity, which Actor created the entry and a text that describes a problem or essentail information about the state of the Actor.
* Http.<br>A Web page shall be available for each Actor. The purpose of the web page is to provide monitoring of an Actor. More advanced web pages that collects information on the overall application (Actors), will be added later.
* Statistics.<br>Statistics is like logging essential for debugging your program. It shall be possible to see how many messages of a given type have been published and how long time has gone sine we received the last message.
* Statemachines<br>State machines are part of nearly all projects . The do however come in many variants and it is always compil
* Behavir Trees<br>
* Reactive programming<br>
* 

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase1.png" height="400"><br>
  Phase1: Focus is to provide different features for Actors.
</p>

The second p

<p align="center">
  <img src="https://github.com/henrik7264/Actors/blob/main/images/Actors_Phase2.png" height="400"><br>
  Phase2: Focus is to provide a distributed environment for sharing messages between Actors.
</p>

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

