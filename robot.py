#!/usr/bin/env python3

import wpilib, wpimath, wpimath.geometry
import phoenix6
from rev import SparkMax, SparkLowLevel, SparkAbsoluteEncoder
from magicbot import MagicRobot

from constant import TunerConstants, DriveConstants, ElevatorConstants

from component.swerve import Swerve
from component.elevator import Elevator

from ntcore import NetworkTableInstance


class Robot(MagicRobot):

    swerve: Swerve
    elevator: Elevator

    def createObjects(self):
        # make controllers
        self.driveController = wpilib.interfaces.GenericHID(0)
        self.operatorController = wpilib.interfaces.GenericHID(1)

        # gyro
        self.gyro = phoenix6.hardware.Pigeon2(TunerConstants._pigeon_id)

        # network tables
        self.nt = NetworkTableInstance.getDefault()

        # encoders
        self.elevatorAbsolute = SparkMax(
            ElevatorConstants.EncoderID, SparkLowLevel.MotorType.kBrushless
        )
        self.elevatorEncoder = self.elevatorAbsolute.getAbsoluteEncoder()

        # motors
        self.elevatorMotor1 = phoenix6.hardware.talon_fx.TalonFX(
            ElevatorConstants.Motor1ID, ElevatorConstants.Motor1Canbus
        )
        self.elevatorMotor2 = phoenix6.hardware.talon_fx.TalonFX(
            ElevatorConstants.Motor2ID, ElevatorConstants.Motor2Canbus
        )

        # followers
        self.elevatorMotor2.set_control(
            phoenix6.controls.follower.Follower(ElevatorConstants.Motor1ID, True)
        )

        # misc
        self.elevatorManualToggle = False

    def teleopPeriodic(self):
        # tid = self.nt.getEntry("/limelight/tid").getDouble(-1)  # Current limelight target id

        if self.driveController.getRawButton(2):
            self.swerve.target(
                wpimath.geometry.Pose2d(
                    0, 0, wpimath.geometry.Rotation2d.fromDegrees(0)
                )
            )

        else:
            self.swerve.go(
                self.driveController.getRawAxis(1),
                self.driveController.getRawAxis(0),
                -self.driveController.getRawAxis(2),
                self.driveController.getRawAxis(3) <= 0,  # field centric toggle
            )

        # elevator movements
        # presets
        if self.operatorController.getRawButton(8):
            self.elevatorManualToggle = not self.elevatorManualToggle

        if self.elevatorManualToggle == False:
            # TODO update preset points
            if self.operatorController.getRawButton(2):
                elevator.set(20)

            elif self.operatorController.getRawButton(3):
                elevator.set(20)

            elif self.operatorController.getRawButton(4):
                elevator.set(20)

        # manual
        else:
            elevator.set(self.operatorController.getRawAxis(0))

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

        if self.driveController.getRawButton(5):
            self.swerve.tare_everything()

        if self.driveController.getRawButton(1):
            self.swerve.brake()
