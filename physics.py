import math
import wpilib
import ntcore

from wpilib import Field2d

# Don't bother if we're not in sim
if wpilib.RobotBase.isSimulation():
    from pyfrc.physics.core import PhysicsInterface

    # from pyfrc.physics.engine import PhysicsEngine
else:
    PhysicsInterface = None
    PhysicsEngine = None

from wpimath.geometry import Pose2d, Rotation2d, Twist2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics

from component.swerve import Swerve
from constant import TunerConstants


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface, robot: "UnnamedToaster"):
        self.physics_controller = physics_controller
        self.swerve: Swerve = robot.swerve  # component/swerve.py

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

        # Update internal pose in swerve sim
        self.swerve.sim_pose = self.robot_pose  # We just manually set the pose (messy)
        self.swerve.gyro.sim_state.set_raw_yaw(
            self.robot_pose.rotation().degrees()
        )  # Proper way to invoke setting the sim state

        # Simulate Limelight outputs
        self.virtual_limelight(self.robot_pose)

        # Update Field2d for visualization
        self.field.setRobotPose(self.robot_pose)

    def virtual_limelight(self, pose: Pose2d):
        """
        Simulates many limelight functions (using nt)
        Written by Joe
        Feel free to add stuff!

        :param pose: The robot's current pose (x, y, heading).
        """

        # Simulate Limelight data
        visible_target = 1  # Target n always visible
        target_offset_x = (
            0  # Horizontal offset in degrees (e.g., perfectly centered target)
        )
        target_offset_y = 0  # Vertical offset in degrees
        target_area = 30.0  # Arbitrary percentage of the image covered by the target

        # Robot pose (pose.x, pose.y, pose.rotation().degrees())
        robot_x = pose.X()
        robot_y = pose.Y()
        robot_heading = pose.rotation().degrees()

        # Get or create the "limelight" NetworkTable
        limelight_table = ntcore.NetworkTableInstance.getDefault().getTable("limelight")

        # Publish Limelight data
        limelight_table.putNumber("tv", visible_target)  # Target visible
        limelight_table.putNumber("tx", target_offset_x)  # Horizontal offset
        limelight_table.putNumber("ty", target_offset_y)  # Vertical offset
        limelight_table.putNumber("ta", target_area)  # Target area

        # Publish simulated pose
        limelight_table.putNumber("botpose_x", robot_x)  # X position
        limelight_table.putNumber("botpose_y", robot_y)  # Y position
        limelight_table.putNumber(
            "botpose_heading", robot_heading
        )  # Heading in degrees
