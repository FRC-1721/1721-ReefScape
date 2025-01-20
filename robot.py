#!/usr/bin/env python3

import wpilib, wpimath, wpimath.geometry
import phoenix6
from magicbot import MagicRobot
import choreo

from constant import TunerConstants, DriveConstants

from component.swerve import Swerve

from ntcore import NetworkTableInstance


class Robot(MagicRobot):

    swerve: Swerve

    def createObjects(self):
        self.controller = wpilib.interfaces.GenericHID(0)
        self.gyro = phoenix6.hardware.Pigeon2(TunerConstants._pigeon_id)
        self.nt = NetworkTableInstance.getDefault()
        self.is_red = (
            lambda: wpilib.DriverStation.getAlliance()
            == wpilib.DriverStation.Alliance.kRed
        )

        try:
            # Latest version only needs this, but pypi doesn't have that
            # version, so when it breaks you can use this line instead
            # self.trajectory = choreo.load_swerve_trajectory("path1")
            self.trajectory = choreo.load_swerve_trajectory(
                os.path.join(wpilib.getDeployDirectory(), "choreo", "path2")
            )
        except ValueError:
            self.trajectory = None

    def teleopPeriodic(self):
        # tid = self.nt.getEntry("/limelight/tid").getDouble(-1)  # Current limelight target id

        if self.controller.getRawButton(2):
            self.swerve.target(
                wpimath.geometry.Pose2d(
                    0, 0, wpimath.geometry.Rotation2d.fromDegrees(0)
                )
            )

        else:
            self.swerve.go(
                self.controller.getRawAxis(1),
                self.controller.getRawAxis(0),
                -self.controller.getRawAxis(2),
                self.controller.getRawAxis(3) <= 0,  # field centric toggle
            )

        # update robot pose based on AprilTags
        # if tid != -1:
        #     pose = self.nt.getEntry("/limelight/botpose_targetspace").getDoubleArray(
        #         [0, 0, 0, 0, 0, 0]
        #     )
        #     self.swerve.add_vision_measurement(
        #         wpimath.geometry.Pose2d(
        #             TODO update robot pose based on AprilTags
        #         ),
        #         phoenix6.utils.get_current_time_seconds(),
        #     )

        if self.controller.getRawButton(5):
            self.swerve.tare_everything()

        if self.controller.getRawButton(1):
            self.swerve.brake()
