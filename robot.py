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

# High Level Components
from component.elevatorControl import ElevatorControl

import util

# Sim
# from physics import PhysicsEngine


class Robot(MagicRobot):
    # high level components should go first
    elevator_control: ElevatorControl

    # components
    swerve: Swerve
    elevator: Elevator
    intake: Intake

    # state machines

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
        self.intakeMotor = IntakeConstants.IntakeMotorClass(
            *IntakeConstants.IntakeMotor
        )

    def teleopPeriodic(self):
        # tid = self.nt.getEntry("/limelight/tid").getDouble(-1)  # Current limelight target id

        # if self.driveController.getRawButton(2):
        #     self.swerve.target(
        #         wpimath.geometry.Pose2d(
        #             0, 0, wpimath.geometry.Rotation2d.fromDegrees(0)
        #         )
        #     )

        # if:
        self.swerve.go(
            -self.driveController.getRawAxis(1),
            -self.driveController.getRawAxis(0),
            self.driveController.getRawAxis(4),
            not self.driveController.getRawButton(5),  # field centric toggle
        )

        if self.driveController.getRawButton(7):
            self.swerve.tare_everything()

        # elevator movements
        # presets
        # if self.operatorController.getRawButton(8):
        if False:
            self.elevator.set_manual_mode(True)
        else:
            self.elevator.set_manual_mode(False)

        if not self.elevator.is_manual_mode():
            # TODO readd if the state machine doesn't work
            # if self.operatorController.getRawButtonPressed(2):
            #     self.elevator.set(EelevConst.Setpoint.MIN_HEIGHT)
            # elif self.operatorController.getRawButtonReleased(2):
            #     self.elevator.set(EelevConst.Setpoint.HOME)

            # if self.operatorController.getRawButtonPressed(3):
            #     self.elevator.set(EelevConst.Setpoint.L2)
            # elif self.operatorController.getRawButtonReleased(3):
            #     self.elevator.set(EelevConst.Setpoint.HOME)

            # if self.operatorController.getRawButtonPressed(4):
            #     self.elevator.set(EelevConst.Setpoint.L1)
            # elif self.operatorController.getRawButtonReleased(4):
            #     self.elevator.set(EelevConst.Setpoint.HOME)

            # Move elevator up and down using PIDs
            if (x := EelevConst.deadzone(self.operatorController.getRawAxis(5))) != 0:
                self.elevator.set(
                    self.elevator.get_position() - (x * EelevConst.dampen),
                )
            if util.value_changed("elevatorX", x) and x == 0:
                self.elevator.set(self.elevator.get_position())

            # ElevatorControl with Setpoints
            if self.operatorController.getRawButtonPressed(3):
                self.elevator_control.start(EelevConst.Setpoint.L2)
            elif self.operatorController.getRawButtonPressed(4):
                self.elevator_control.start(EelevConst.Setpoint.L1)

        else:
            # Manual mode
            self.elevator.set(
                -self.operatorController.getRawAxis(5) * EelevConst.manualdampen
                + (
                    EelevConst.stay
                    if self.elevatorMotor.get_position().value < 3
                    else 0
                )
            )

        # INTAKE movements
        if self.operatorController.getRawButton(5):
            self.intake.intake()
        elif self.operatorController.getRawButton(6):
            self.intake.eject()

        if (self.operatorController.getRawAxis(2) >= 0.05) == True:
            self.ShooterControl.set(IntakeConstants.PosOut)
        else:
            self.intake.set(IntakeConstants.PosIn)

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
