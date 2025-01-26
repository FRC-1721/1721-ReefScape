[![Robot Workflow](https://github.com/FRC-1721/1721-ReefScape/actions/workflows/robot-workflow.yml/badge.svg)](https://github.com/FRC-1721/1721-ReefScape/actions/workflows/robot-workflow.yml)

# 1721-ReefScape

# Development

## Setting up

Everyone on the code team should be able to develop the robot code! But the first step
is making sure you're on the same page and have all the available dev tools.


### Cloning this repo

Clearly, we're using git to manage the robot software. Make an account on github, install `git` for your system and 
clone this repository

```shell
git clone https://github.com/FRC-1721/1721-ReefScape
cd 1721-ReefScape
```

#### Note on ssh

You're welcome to use ssh if you have that setup. But the school blocks ssh traffic on the normal port
use ssh over https by editing your `~/.ssh/config` like this:

```
# Github
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
    IdentityFile path/to/my/identityfile
```


### Text Editors

You can use any text editor you like but we recommend `vscode` or `vim` (or `emacs` if you want to make Dylan happy).
Whatever editor you use please comment and format your code! We use `black` to enforce python style.


### Pipenv

We use `pipenv` to manage our python dependencies, and keep everyone's env in sync. Download and install pipenv from 
a package maintainer or via pip `pip install pipenv` and then setup your environment like this:

```shell
pipenv install
pipenv shell
```


### Using the Simulator

Running the simulator is not just a useful exercise, it also ensures that you have all dependencies installed,
all libs are functional, and that your system supports the necessary requirements to simulate the robot 
and its hardware. To make development easier we use a `Makefile` at the root of this repo to automate 
dev tools. Invoke the simulator with:

```shell
make sim
```

### VSCode
Start the VSCode editor from the command line, with full access to the dependencies, by doing the following:
- Go to the directory where the git code is located
- pipenv install
- pipenv shell
- code .

The VSCode debugger can be used by creating a new launch.json and adding the folloiwng: (this will add two choices, 1 for launching the simulator and 1 for launching the tests):

{
   // Use IntelliSense to learn about possible attributes.
   // Hover to view descriptions of existing attributes.
   // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
   "version": "0.2.0",
   "configurations": [


       {
           "name": "Sim",
           "type": "debugpy",
           "request": "launch",
           "module": "robotpy",
           "console": "integratedTerminal",
           "args": [
               "sim"
           ]
       },
       {
           "name": "Tests",
           "type": "debugpy",
           "request": "launch",
           "module": "robotpy",
           "console": "integratedTerminal",
           "args": [
               "test"
           ]
       }       
   ]
}

### Other Notes

Please assume-unchanged for local ds json config values. This will help prevent constantly overwriting 
these files in general use/tweaking. If you do make a change to the simgui files, you can always
overwrite the assume-unchanged by invoking `git add -f <file>`

```shell
git update-index --assume-unchanged simgui-ds.json simgui.json simgui-window.json
```

## What if something goes wrong?

Report a bug, issue or missing feature! The most helpful way to track and alert the code team is via
[github issues](https://github.com/FRC-1721/1721-ReefScape/issues/new).
