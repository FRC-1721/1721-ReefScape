import math
import wpilib
import logging

from wpilib import Field2d
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Twist2d
from wpimath.kinematics import SwerveDrive4Kinematics, SwerveModuleState

from constant import TunerConstants, DriveConstants


class PhysicsEngine:
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.swerve = None

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
        # Simulate simple linear and rotational motion
        linear_speed = 2.0  # meters per second
        angular_speed = math.radians(45)  # radians per second (45 degrees per second)

        # Calculate the change in position and rotation
        dx = linear_speed * timestep
        dy = 0  # No sideways motion for simplicity
        dtheta = angular_speed * timestep

        # Use Twist2d for pose updates
        twist = Twist2d(dx, dy, dtheta)
        self.robot_pose = self.robot_pose.exp(twist)

        # Update Field2d for visualization
        self.field.setRobotPose(self.robot_pose)
