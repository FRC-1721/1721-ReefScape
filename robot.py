#!/usr/bin/env python3

# Libs
import logging
import wpilib, wpimath, wpimath.geometry
import phoenix6

# from rev import SparkMax, SparkLowLevel, SparkAbsoluteEncoder
from magicbot import MagicRobot
from ntcore import NetworkTableInstance

from constant import TunerConstants, DriveConstants, IntakeConstants
import constant.ElevatorConstants as EelevConst

# Components
from component.swerve import Swerve
from component.elevator import Elevator
from component.intake import Intake

import util

# Sim
# from physics import PhysicsEngine


class Robot(MagicRobot):

    swerve: Swerve
    elevator: Elevator
    intake: Intake

    def robotInit(self):
        super().robotInit()

        # Configure logging
        logging.basicConfig(
            level=logging.INFO if wpilib.RobotBase.isSimulation() else logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Robot")
        self.logger.info("Robot is initializing...")

    def createObjects(self):
        # Controllers
        self.driveController = wpilib.interfaces.GenericHID(0)
        self.operatorController = wpilib.interfaces.GenericHID(1)

        # Gyro
        self.gyro = phoenix6.hardware.Pigeon2(TunerConstants._pigeon_id)

        # NetworkTables
        self.nt = NetworkTableInstance.getDefault()

        # Motors - (Elevator Injection)
        self.elevatorMotor = EelevConst.MotorClass(
            EelevConst.Motor1ID, EelevConst.Motor1Canbus
        )
        self.elevatorMotor2 = EelevConst.MotorClass(
            EelevConst.Motor2ID, EelevConst.Motor2Canbus
        )
        # Set motor2 to follow motor1
        self.elevatorMotor2.set_control(
            phoenix6.controls.follower.Follower(EelevConst.Motor1ID, False)
        )
        self.elevatorMotor.set_position(0)  # Reset Falcon's built-in encoder
        self.elevatorMotor.configurator.apply(EelevConst.config)

        # Intake Motors
        self.posMotor = IntakeConstants.PosMotorClass(*IntakeConstants.PosMotor)
        self.posMotor.set_position(-29)
        self.intakeMotor = IntakeConstants.IntakeMotorClass(
            *IntakeConstants.IntakeMotor
        )

        self.elevatorLimit = EelevConst.LimitClass(EelevConst.LimitID)

    def teleopPeriodic(self):
        # tid = self.nt.getEntry("/limelight/tid").getDouble(-1)  # Current limelight target id

        # if self.driveController.getRawButton(2):
        #     self.swerve.target(
        #         wpimath.geometry.Pose2d(
        #             0, 0, wpimath.geometry.Rotation2d.fromDegrees(0)
        #         )
        #     )

        # if:
        dampen = 1
        if pos := self.elevator.get_position() > 5:
            dampen -= max((pos - 5) / 15, 0.3)
        self.swerve.go(
            self.driveController.getRawAxis(1) * dampen,
            self.driveController.getRawAxis(0) * dampen,
            self.driveController.getRawAxis(4) * dampen,
            not self.driveController.getRawButton(5),  # field centric toggle
        )

        if self.driveController.getRawButton(7):
            self.swerve.tare_everything()

        # elevator movements
        if (
            True
            # self.intakeMotor.get_position().value < -5
        ):
            if self.operatorController.getRawButtonPressed(2):
                self.elevator.set(EelevConst.Setpoint.MIN_HEIGHT)
            if self.operatorController.getRawButtonReleased(2):
                self.elevator.set(EelevConst.Setpoint.HOME)

            if self.operatorController.getRawButtonPressed(3):
                self.elevator.set(EelevConst.Setpoint.L2)
            if self.operatorController.getRawButtonReleased(3):
                self.elevator.set(EelevConst.Setpoint.HOME)

            if self.operatorController.getRawButtonPressed(4):
                self.elevator.set(EelevConst.Setpoint.L1)
            if self.operatorController.getRawButtonReleased(4):
                self.elevator.set(EelevConst.Setpoint.HOME)

            if (x := EelevConst.deadzone(self.operatorController.getRawAxis(5))) != 0:
                self.elevator.x = max(
                    0,
                    self.elevatorMotor.get_position().value
                    - (x * 3 * EelevConst.dampen),
                )
            if util.value_changed("elevatorX", x) and x == 0:
                self.elevator.x = self.elevator.get_position()

        # INTAKE movements
        if self.operatorController.getRawButton(5):
            self.intake.intake()
        if self.operatorController.getRawButton(6):
            self.intake.eject()

        # TODO clean this up
        if self.operatorController.getRawAxis(2) >= 0.1:
            self.intake.set(IntakeConstants.PosOut)
        elif self.operatorController.getRawAxis(3) >= 0.1:
            self.intake.set(IntakeConstants.PosIn)
        # elif ????:
        #    intake.goal(IntakeConstants.PosHome)

        # self.intake.set(IntakeConstants.clamp(x * IntakeConstants.PosDampen))

        # self.posMotor.set(
        #     self.operatorController.getRawAxis(1) * IntakeConstants.PosDampen
        # )

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

        if (
            self.driveController.getRawAxis(2) > 0.5
            or self.driveController.getRawAxis(3) > 0.5
        ):
            self.swerve.brake()
