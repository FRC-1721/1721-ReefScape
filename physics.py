import math
import wpilib

from wpilib import Field2d
from pyfrc.physics.core import PhysicsInterface
from wpimath.geometry import Pose2d, Rotation2d, Twist2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from constant import TunerConstants


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface, robot: "UnnamedToaster"):
        self.physics_controller = physics_controller
        self.swerve = robot.swerve  # component/swerve.py

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
        # Get the current module states from the swerve component
        module_states = tuple(self.swerve.get_state().module_targets)
        # (Requires packing because of pre-build pheonix6 stuff.. idk)

        # Use the kinematics model to calculate the robot's chassis speeds
        chassis_speeds = self.swerve_kinematics.toChassisSpeeds(module_states)

        # Convert chassis speeds into a twist
        twist = Twist2d(
            chassis_speeds.vx * timestep,
            chassis_speeds.vy * timestep,
            chassis_speeds.omega * timestep,
        )

        # Update the robot pose
        self.robot_pose = self.robot_pose.exp(twist)

        # Update Field2d for visualization
        self.field.setRobotPose(self.robot_pose)
