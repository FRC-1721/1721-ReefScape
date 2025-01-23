#!/usr/bin/env python3

import wpilib, wpimath, wpimath.geometry
import phoenix6
from magicbot import MagicRobot

from constant import TunerConstants, DriveConstants, ElevatorConstants

from component.swerve import Swerve

from ntcore import NetworkTableInstance


class Robot(MagicRobot):

    swerve: Swerve

    def createObjects(self):
        self.controller = wpilib.interfaces.GenericHID(0)
        self.gyro = phoenix6.hardware.Pigeon2(TunerConstants._pigeon_id)
        self.nt = NetworkTableInstance.getDefault()

        # motors
        self.elevatorMotor1 = phoenix6.hardware.talon_fx.TalonFX(
            ElevatorConstants.Motor1ID, ElevatorConstants.Motor1Canbus
        )
        self.elevatorMotor2 = phoenix6.hardware.talon_fx.TalonFX(
            ElevatorConstants.Motor2ID, ElevatorConstants.Motor2Canbus
        )

        # encoders
        self.elevatorEncoder = phoenix6.hardware.CANcoder(
            ElevatorConstants.EncoderID, ElevatorConstants.EncoderCanbus
        )

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
        #             TODO
        #         ),
        #         phoenix6.utils.get_current_time_seconds(),
        #     )

        if self.controller.getRawButton(5):
            self.swerve.tare_everything()

        if self.controller.getRawButton(1):
            self.swerve.brake()
