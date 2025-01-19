#!/usr/bin/env python3

import wpilib
import phoenix6
from magicbot import MagicRobot

from constant import TunerConstants, DriveConstants

from component.swerve import Swerve


class Robot(MagicRobot):

    swerve: Swerve

    def createObjects(self):
        self.controller = wpilib.interfaces.GenericHID(0)

    def teleopPeriodic(self):
        self.swerve.go(
            self.controller.getRawAxis(0),
            self.controller.getRawAxis(1),
            self.controller.getRawAxis(2),
        )

        if self.controller.getRawButton(1):
            self.swerve.brake()
