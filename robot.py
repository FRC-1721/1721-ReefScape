#!/usr/bin/env python3

# Libs
import logging
import wpilib, wpimath, wpimath.geometry
import phoenix6

# from rev import SparkMax, SparkLowLevel, SparkAbsoluteEncoder
from magicbot import MagicRobot
from ntcore import NetworkTableInstance

from constant import TunerConstants, DriveConstants
import constant.ElevatorConstants as EelevConst

# Components
from component.swerve import Swerve
from component.elevator import Elevator

# Sim
# from physics import PhysicsEngine


class Robot(MagicRobot):

    swerve: Swerve
    elevator: Elevator

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
        # if True:
        if self.operatorController.getRawButton(8):
            self.elevator.set_manual_mode(True)
        else:
            self.elevator.set_manual_mode(False)

        if not self.elevator.is_manual_mode():
            # TODO update preset points
            if self.operatorController.getRawButton(2):
                self.elevator.set(EelevConst.Setpoint.MIN_HEIGHT)

            elif self.operatorController.getRawButton(3):
                self.elevator.set(EelevConst.Setpoint.LOW)

            elif self.operatorController.getRawButton(4):
                self.elevator.set(EelevConst.Setpoint.HIGH)
        else:
            # Manual mode
            if self.operatorController.getRawButton(7):
                if self.operatorController.getRawButton(4):
                    print("UP")
                    self.elevator.set(EelevConst.up)

                elif self.operatorController.getRawButton(1):
                    print("DOWN")
                    self.elevator.set(EelevConst.down)

                else:
                    if self.elevator.get_position() > 0.1:
                        self.elevator.set(EelevConst.stay)
            else:
                self.elevator.set(
                    self.operatorController.getRawAxis(0) * EelevConst.dampen
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

        if self.driveController.getRawButton(5):
            self.swerve.tare_everything()

        if self.driveController.getRawButton(1):
            self.swerve.brake()
