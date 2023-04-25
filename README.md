# Actors
Dear all,

Welcome to an Actors library for C++/Python. You will very soon realize that this is much more that just a library for creating Actors - my hope with this project is to create a framework for creating spectacular software systems.

## Motivation
The idea with this library is to create a framework for creating highly performant, scalable and maintainable code. My inspiration for this project originates from the following sources:

* Actors Model (https://en.wikipedia.org/wiki/Actor_model)
* ROS (https://www.ros.org)
* RxROS (https://github.com/rosin-project/rxros)
* RxROS2 (https://github.com/rosin-project/rxros2)
* Reactive Programming (https://reactivex.io)
* Reactive systems (https://www.reactivemanifesto.org)

The Actors library has noting to do with programming robots, although all the references to ROS. It is a general purpose library/framework for creating reactive systems.

## Idea

* Low coupling/high cohesion
* Reusability
* Keep it simple

## Installation and Setup
The Actors library is dependand on the ReactiveX extensions RxPY (see https://github.com/ReactiveX/RxPY) and RxCpp (see https://github.com/ReactiveX/RxCpp). These two extensions must therefore be installed prior to installing the Actors library. The insrallation process is as follows:

1. Install RxPy
2. Install RxCPP
3. Install Actor

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

### Installation of the Actors library om Linux

```bash
https://github.com/henrik7264/Actors.git
```

#### Testing the Python Actors library on Linux

```bash
cd Actors/py_actors
export PYTHONPATH=`pwd`
python3 example_publisher_subscriber/main.py
python3 example_statemachine/main2.py
```

