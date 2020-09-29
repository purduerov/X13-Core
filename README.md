# X13-Core
Codebase for the the X13 version of the ROV

Software Versions
Ubuntu 18
Raspbian Buster
ROS Melodic

Hardware
Raspberry Pi 4

## Getting ROS to work with Python 3
Previous X repos have ROS working both with Python 2 and 3. This behavior is determined by the shebang (e.g. `#!/usr/bin/python`) at the top of relevant ROS scripts. These should be set to `#!/path/to/python3` going forward.

If you already have ROS Kinetic installed, I would highly recommend wiping it with `sudo apt remove ros-*` and removing any dependencies installed with it with `sudo apt autoremove`. This works if Kinetic was installed with apt in the first place.

If Kinetic was compiled from source, simply delete the `catkin_ws` folder (or whatever you named it) and any `source`s in your .bashrc if you added them.

### Table of Contents
* Install/Upgrade
    1. [Existing Melodic Install](#ros-melodic-already-installed)
    2. [Fresh Install](#fresh-install)
    3. [Compile from Source](#compile-from-source)
* [Troubleshooting](#troubleshooting)

### ROS Melodic Already Installed
This assumes Melodic was installed with `apt` and not compiled from source. If it was compiled from source, delete the install directory, and follow [these instructions](#compile-from-source).

1. Install Python 3 ROS dependencies with pip3

    Make sure pip3 is installed in the first place with `sudo apt install python3-pip`.
    
    Run `sudo pip3 install -U rosdep rosinstall_generator vcstool rosinstall`. Note the use of `pip3`.

    Optional: Remove Python 2 versions of above tools with `sudo apt remove python-ros* python-wstool`

2. Set the environment variable `ROS_PYTHON_VERSION` to 3

    Run `export ROS_PYTHON_VERSION=3`.

3. Update dependencies

    Run `sudo rosdep init` to find where the dependency list file is.

    Delete that file.

    Run `sudo rosdep init` again.

    Run `rosdep update`.

You should now have everything ready to go. Simply add the `source` line to your .bashrc file to make life easier for every time you open a terminal window.
    
### Fresh Install

1. Follow the [standard instructions](http://wiki.ros.org/melodic/Installation/Ubuntu) up to but **NOT** including 1.4 (i.e Install Step)
2. Set the environment variable `ROS_PYTHON_VERSION` to 3

    Run `export ROS_PYTHON_VERSION=3`.

    I'm not sure how necessary it is at this stage, but it is required down the line anyway.

3. Install ROS Melodic

    Full: `sudo apt install ros-melodic-desktop-full` (Recommended by Ivan because this was tested)

    Regular: `sudo apt install ros-melodic-desktop` (Recommended on ROS Wiki, but should work just the same)

    Base: `sudo apt install ros-melodic-ros-base` (Why?)

4. Install Python 3 dependencies

    Run `sudo pip3 install -U rosdep rosinstall_generator vcstool rosinstall`. Note the use of `pip3`.

5. Init/Update ROS dependencies

    Run `sudo rosdep init`

    Run `rosdep update`

Everything should be set up now. Remember to `source` your install of ROS.

### Compile from Source
Oh dear, what are you doing here? These are only meant for those working with Ubuntu versions **other than 18.04**. When I compiled from source, I was using Ubuntu 19.04, so bear that in mind. If you have nothing else going on your Ubuntu install, I would **highly** recommend wiping it and getting 18.04 instead. If you're crazy like, welcome.

1. Install Python 3 dependencies

    Run `sudo pip3 install -U rosdep rosinstall_generator vcstool rosinstall`. Note the use of `pip3`.

2. Set the environment variable `ROS_PYTHON_VERSION` to 3

    Run `export ROS_PYTHON_VERSION=3`.

3. Init/Update ROS dependencies

    Run `sudo rosdep init`

    Run `rosdep update`

3. Create a catkin workspace

    Make a directory somewhere (e.g. `mkdir ~/some_name_like_ROS_install`)

    Go into it `cd ~/some_name_like_ROS_install`

    Make a src directory `mkdir src`

4. Fetch relevant files

    Again, this is following step-by-step of what I did, so I'm only covering Full Desktop install, but the process should be the same for other versions

    Run `rosinstall_generator desktop_full --rosdistro melodic --deps --tar > melodic-desktop-full.rosinstall`

    Run `vcs import src < melodic-desktop-full.rosinstall`

5. Resolve dependencies

    There is a trick to this step. You're essentially tricking `rosdep` into thinking you're on 18.04.

    Run `rosdep install --from-paths src --ignore-src --rosdistro melodic -y --os=ubuntu:bionic`

    Very important to add `--os=ubuntu:bionic`.

6. Build it
    
    Run `./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release`

After what seems like an eternity (about 30 minutes for me), you should have a working install of ROS Melodic compiled. All that is left is to add the setup.bash script to your .bashrc file for an easy life.

### Troubleshooting
* Something went wrong during installation
    
    This should only be an issue if you're compiling from source or attempting to install with apt on anything other than Ubuntu 18.04. For the former, I have no answer. For the latter, I recommend installing 18.04 or following [Compile from Source](#compile-from-source) instructions.

* catkin_make fails 70-90% way through a workspace

    If this is in X12, some files still contain python shebangs. Try changing them to python3 ones.
    If that still doesn't work, it might be more of an issue of using code that was written with Kinetic.

In all cases, especially if you have had previous ROS installs on your machine, make sure `rosdep init`'s file is up-to-date with Python 3 dependencies. Meaning run `rosdep init` to find the file and delete it. Run that command again and run `rosdep update`. You may need to use `sudo` with the init stage.