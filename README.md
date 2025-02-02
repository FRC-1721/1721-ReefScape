[![Robot Workflow](https://github.com/FRC-1721/1721-ReefScape/actions/workflows/robot-workflow.yml/badge.svg)](https://github.com/FRC-1721/1721-ReefScape/actions/workflows/robot-workflow.yml)
# 1721-ReefScape

![beyblade](https://github.com/user-attachments/assets/2c38aa06-f3b5-47c6-af1f-6b957e582218)


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
