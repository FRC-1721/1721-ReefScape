#!/usr/bin/env python3

# Libs
import logging
import math
import os
import wpilib, wpimath, wpimath.geometry
import phoenix6

# from rev import SparkMax, SparkLowLevel, SparkAbsoluteEncoder
from magicbot import MagicRobot
from ntcore import NetworkTableInstance

from constant import TunerConstants, DriveConstants, IntakeConstants, ClimberConstants
import constant.ElevatorConstants as EelevConst
from constant.ControllerConstants import DriverConstants, OperatorConstants

# Components
from component.swerve import Swerve
from component.elevator import Elevator
from component.intake import Intake
from component.climber import Climber

# High Level Components
from component.elevatorControl import ElevatorControl

import util
import choreo

# Sim
# from physics import PhysicsEngine


class Robot(MagicRobot):
    # high level components should go first
    elevator_control: ElevatorControl

    # components
    swerve: Swerve
    elevator: Elevator
    intake: Intake
    climber: Climber

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
        wpilib.cameraserver.CameraServer().launch()

        self.is_red = (
            lambda: wpilib.DriverStation.getAlliance()
            == wpilib.DriverStation.Alliance.kRed
        )

        # Controllers
        self.driveController = DriverConstants.controller
        self.operatorController = OperatorConstants.controller

        # Gyro
        self.gyro = phoenix6.hardware.Pigeon2(TunerConstants._pigeon_id)

        # NetworkTables
        self.nt = NetworkTableInstance.getDefault()

        # Motors - (Elevator Injection)
        self.elevatorMotor = EelevConst.MotorClass(*EelevConst.Motor1)
        self.elevatorMotor2 = EelevConst.MotorClass(*EelevConst.Motor2)
        self.elevatorMotor2.set_control(
            phoenix6.controls.follower.Follower(EelevConst.Motor1ID, False)
        )  # motor2 follows motor1
        self.elevatorMotor.set_position(0)  # Reset Falcon's built-in encoder
        self.elevatorMotor.configurator.apply(EelevConst.config)
        self.elevatorMotor.configurator.apply(EelevConst.PIDConfig)

        # Intake Motors
        self.posMotor = IntakeConstants.PosMotorClass(*IntakeConstants.PosMotor)
        self.posMotor.set_position(0)
        self.posMotor.configurator.apply(IntakeConstants.PIDConfig)

        self.intakeMotor = IntakeConstants.IntakeMotorClass(
            *IntakeConstants.IntakeMotor
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

        self.elevatorLimit = EelevConst.LimitClass(EelevConst.LimitID)

        self.climbMotor = ClimberConstants.MotorClass(*ClimberConstants.Motor)

    def teleopPeriodic(self):
        # dampen if elevator is up
        dampen = 1
        if pos := self.elevator.get_position() > 5:
            dampen -= max((pos - 5) / 15, 0.3)

        speeds = [
            self.driveController.getRawAxis(DriverConstants.driveFD) * dampen,
            self.driveController.getRawAxis(DriverConstants.driveLR) * dampen,
            self.driveController.getRawAxis(DriverConstants.driveTR) * dampen,
        ]
        speeds = list(map(util.squaredampen, speeds))

        if self.driveController.getRawButton(DriverConstants.driveSlow):
            speeds = list(map(lambda x: util.squaredampen(x) * 0.5, speeds))
        self.swerve.go(
            *speeds,
            not self.driveController.getRawButton(5),  # field centric toggle
        )

        if self.driveController.getRawButton(2):
            self.swerve.goal_pose = self.swerve.get_state_copy().pose
        if self.driveController.getRawButtonPressed(1):
            self.swerve.resetControllers()
        if self.driveController.getRawButton(1):
            if self.swerve.goal_pose:
                self.swerve.target(self.swerve.goal_pose)

        # tare
        if self.driveController.getRawButton(DriverConstants.tare):
            self.swerve.tare_everything()
            self.gyro.reset()

        # elevator movements
        if self.operatorController.getRawButtonPressed(OperatorConstants.home):
            self.elevator.set(EelevConst.Setpoint.HOME)
        if self.operatorController.getRawButtonPressed(OperatorConstants.l1):
            self.elevator.set(EelevConst.Setpoint.L1)
        if self.operatorController.getRawButtonPressed(OperatorConstants.l2):
            self.elevator.set(EelevConst.Setpoint.L2)
        if self.operatorController.getRawButtonPressed(OperatorConstants.maxHeight):
            self.elevator.set(EelevConst.Setpoint.L3)

        # manual mode elevationizer
        if (
            x := util.squaredampen(
                EelevConst.deadzone(
                    self.operatorController.getRawAxis(
                        OperatorConstants.elevatorManualAxis
                    )
                )
            )
        ) != 0:
            self.elevator.x = max(
                0,
                self.elevatorMotor.get_position().value - (x * 8 * EelevConst.dampen),
            )
        if util.value_changed("elevatorX", x) and x == 0:
            self.elevator.x = self.elevator.get_position()

        # INTAKE actions
        if self.operatorController.getRawButton(OperatorConstants.intake):
            self.intake.intake()
        if self.operatorController.getRawButton(OperatorConstants.eject):
            self.intake.eject()
        if self.operatorController.getRawButton(OperatorConstants.hold):
            self.intake.hold()

        # PID intake movement
        if self.operatorController.getRawAxis(OperatorConstants.PosOut) >= 0.1:
            self.intake.set(IntakeConstants.PosOut)

        elif self.operatorController.getRawAxis(OperatorConstants.PosIn) >= 0.1:
            self.intake.set(IntakeConstants.PosIn)

        # manual intake movement
        if (
            x := util.squaredampen(
                IntakeConstants.deadzone(
                    self.operatorController.getRawAxis(
                        OperatorConstants.intakeManualAxis
                    )
                )
            )
        ) != 0:
            self.intake.x = self.intake.pos() - (x * 6)
        if util.value_changed("intakeposX", x) and x == 0:
            self.intake.x = self.intake.pos()

        # climber movement
        if self.operatorController.getPOV() == OperatorConstants.climb:
            self.climber.climb()
            # self.climbMotor.set(0.1)

        if self.operatorController.getPOV() == OperatorConstants.unclimb:
            self.climber.unclimb()
            # self.climbMotor.set(-0.1)

        # You need to give the limelight the current yaw value in
        # order for MegaTag2 to accurately estimate the robot pose
        # There is supposed to be a function for this in limelightlib but
        # it only exists in the Java library, so we have to do this manually
        self.nt.getEntry("/limelight/robot_orientation_set").setDoubleArray(
            # [self.swerve.get_state().pose.rotation().degrees(), 0, 0, 0, 0, 0]
            [
                self.swerve.heading(),
                self.swerve.get_state().speeds.omega_dps,
                0,
                0,
                0,
                0,
            ]
        )
        self.nt.flush()  # Give limelight the pose immediately (don't wait)

        # update robot pose based on AprilTags
        tid = self.nt.getEntry("/limelight/tid").getDouble(-1)
        if tid != -1:
            # we have to use botpose_orb_wpiblue cuz why not
            pose = self.nt.getEntry("/limelight/botpose_orb_wpiblue").getDoubleArray(
                [0 for i in range(25)]
            )
            self.swerve.add_vision_measurement(
                wpimath.geometry.Pose2d(pose[0], pose[1], pose[5] * (math.pi / 180)),
                phoenix6.utils.get_current_time_seconds()
                - (pose[6] * 0.001),  # pose[6] is latency
            )

        # brake
        if (
            self.driveController.getRawAxis(DriverConstants.brake[0]) > 0.5
            or self.driveController.getRawAxis(DriverConstants.brake[1]) > 0.5
        ):
            self.swerve.brake()
