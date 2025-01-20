import math
import wpilib
import logging

from wpilib import Field2d
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics, SwerveModuleState

from constant import TunerConstants, DriveConstants


class PhysicsEngine:
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller

        # Define the swerve module locations from constants
        self.module_locations = [
            Translation2d(module.location_x, module.location_y)
            for module in (
                TunerConstants.front_left,
                TunerConstants.front_right,
                TunerConstants.back_left,
                TunerConstants.back_right,
            )
        ]

        # Create kinematics model for swerve drivetrain
        self.swerve_kinematics = SwerveDrive4Kinematics(*self.module_locations)

        # Simulate drivetrain motion
        self.robot_pose = Pose2d(0, 0, Rotation2d(0))  # Starting pose
        self.field = Field2d()
        wpilib.SmartDashboard.putData("Field", self.field)

    def update_sim(self, now, timestep):
        try:
            swerve = self.physics_controller.swerve
        except AttributeError:
            wpilib.reportWarning("Swerve subsystem not yet initialized!", False)
            return

        # Fetch chassis speeds from the swerve subsystem
        chassis_speeds = swerve.get_chassis_speeds()

        # Calculate module states (kinematics only, no motor dynamics)
        module_states = self.swerve_kinematics.toSwerveModuleStates(chassis_speeds)
        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            module_states, DriveConstants.max_speed
        )

        # Simulate the robot pose over the timestep
        delta_pose = Pose2d(
            chassis_speeds.vx * timestep,
            chassis_speeds.vy * timestep,
            Rotation2d(chassis_speeds.omega * timestep),
        )
        self.robot_pose = self.robot_pose + delta_pose

        # Update Field2d and NetworkTables for visualization
        self.field.setRobotPose(self.robot_pose)
        nt = wpilib.NetworkTableInstance.getDefault()
        pose_table = nt.getTable("Pose")
        pose_table.putNumber("X", self.robot_pose.X())
        pose_table.putNumber("Y", self.robot_pose.Y())
        pose_table.putNumber(
            "Heading", math.degrees(self.robot_pose.rotation().radians)
        )
