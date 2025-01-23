#!/usr/bin/env python3
import os

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
        self.savePosition = wpimath.geometry.Pose2d(
            0, 0, wpimath.geometry.Rotation2d.fromDegrees(0)
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
        # You need to give the limelight the current yaw value in
        # order for MegaTag2 to accurately estimate the robot pose
        # There is supposed to be a function for this in limelightlib but
        # it only exists in the Java library, so we have to do this manually
        self.nt.getEntry("/limelight/robot_orientation_set").setDoubleArray(
            [self.swerve.get_state().pose.rotation().degrees(), 0, 0, 0, 0, 0]
            # [self.gyro.getRotation2d().degrees(), 0, 0, 0, 0, 0]
        )
        self.nt.flush()  # Give limelight the pose immediately (don't wait)

        tid = self.nt.getEntry("/limelight/tid").getDouble(-1)
        if tid != -1:  # Ignore pose if no target is in the camera
            # MegaTag 2 position estimates have "orb" in the name (correct me if I'm wrong)
            entry = (
                "/limelight/botpose_orb_wpiblue"
                if not self.controller.getRawButton(8)
                else "/limelight/botpose_wpiblue"
            )
            pose = self.nt.getEntry(entry).getDoubleArray([0, 0, 0, 0, 0, 0])
            # I think something might be wrong here
            self.swerve.add_vision_measurement(
                wpimath.geometry.Pose2d(
                    wpimath.geometry.Translation2d(pose[0], pose[1]),
                    wpimath.geometry.Rotation2d.fromDegrees(pose[5]),
                ),
                phoenix6.utils.get_current_time_seconds(),
            )

        # We don't have to include logic to only give one SwerveRequest at a time
        # because only one SwerveRequest can be executed at a time.
        # I check for the brake being pressed last because I think it is the most important
        self.swerve.go(
            self.controller.getRawAxis(1),
            self.controller.getRawAxis(0),
            -self.controller.getRawAxis(2),
            self.controller.getRawAxis(3) <= 0,  # field centric toggle
        )

        # For testing, save a position with button 4 and go to the position with button 2
        # TODO Fix field relative pose data and swerve.target() going to the wrong place
        # Positioning currently doesn't work and using swerve.target() to go to a pose
        # causes the robot to go to a very different location that is not the target
        # Be careful testing this because it will cause the robot to move very fast
        # in a random direction
        # TODO Put self.savePosition on NT
        if self.controller.getRawButton(4):
            self.savePosition = self.swerve.get_state().pose
        if self.controller.getRawButton(2):
            self.swerve.target(self.savePosition)
        if self.controller.getRawButton(7):
            self.savePosition.x += 1

        if self.controller.getRawButton(10):  # Go to the start pose of the loaded Auto
            self.swerve.target(self.trajectory.get_initial_pose(False))

        # print(
        #     "----------------------------------------\n"
        #     + str(self.savePosition)
        #     + "\n"
        #     + str(self.swerve.get_state().pose)
        # )

        # careful
        if self.controller.getRawButton(5):
            self.swerve.tare_everything()
            self.gyro.reset()
        if self.controller.getRawButton(6):
            self.gyro.reset()
        if self.controller.getRawButton(1):
            self.swerve.brake()
