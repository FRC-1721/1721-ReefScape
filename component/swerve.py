import logging
import math
import wpilib
import wpimath, wpimath.controller, wpimath.trajectory
import phoenix6

from magicbot import feedback, will_reset_to
from wpimath.geometry import Pose2d

from constant import TunerConstants, DriveConstants


class Swerve(phoenix6.swerve.SwerveDrivetrain):

    gyro: phoenix6.hardware.Pigeon2
    request = will_reset_to(
        phoenix6.swerve.requests.Idle()
    )  # default request if no request is given

    # TODO: Adjust PIDs?
    # xcontroller = wpimath.controller.ProfiledPIDController(
    #     0.6, 0.2, 0.1, wpimath.trajectory.TrapezoidProfile.Constraints(0.5, 1), 0.01
    # )
    # ycontroller = wpimath.controller.ProfiledPIDController(
    #     0.6, 0.2, 0.1, wpimath.trajectory.TrapezoidProfile.Constraints(0.5, 1), 0.01
    # )
    xcontroller = wpimath.controller.PIDController(0.6, 0.2, 0.1, 0.01)
    ycontroller = wpimath.controller.PIDController(0.6, 0.2, 0.1, 0.01)
    spinner = wpimath.controller.PIDController(0.8, 0.0, 0.0, 0.01)
    # controller = HolonomicDriveController(
    #     PIDController(1, 0, 0),
    #     PIDController(1, 0, 0),
    #     ProfiledPIDControllerRadians(
    #         1, 0, 0, TrapezoidProfileRadians.Constraints(6.28, 3.14)
    #     ),
    # )

    def __init__(self):
        phoenix6.swerve.SwerveDrivetrain.__init__(
            self,
            TunerConstants._drive_motor_class,
            TunerConstants._steer_motor_class,
            TunerConstants._encoder_class,
            TunerConstants.drivetrain_constants,
            [
                TunerConstants.front_left,
                TunerConstants.front_right,
                TunerConstants.back_left,
                TunerConstants.back_right,
            ],
        )

        if phoenix6.utils.is_simulation() or not wpilib.RobotBase.isReal():
            self.sim_pose = Pose2d(0, 0, 0)

            # Dynamically create a new object that mimics the behavior of get_state but overrides only the pose
            _orig_get_state = self.get_state  # Store the original get_state method

            # Overwrite only the pose attribute (messy but this only happens in sim!)
            self.get_state = lambda: type(
                "State", (), {**vars(_orig_get_state()), "pose": self.sim_pose}
            )()
            logging.warning("Swerve is running in sim mode!")

        self.goal_pose = wpimath.geometry.Pose2d(0, 0, 0)
        self.spinner.enableContinuousInput(-math.pi, math.pi)

        self.resetControllers()

        self.pid_info = "Not Started!"

    def resetControllers(self):
        self.xcontroller.reset()
        self.ycontroller.reset()
        self.spinner.reset()

    def go(self, x, y, z, field_centric=False):  # convenience
        self.request = (
            (
                phoenix6.swerve.requests.FieldCentric().with_forward_perspective(  # you can only forward perspective with field relative
                    phoenix6.swerve.requests.ForwardPerspectiveValue.OPERATOR_PERSPECTIVE
                )
                if field_centric
                else phoenix6.swerve.requests.RobotCentric()
            )
            .with_deadband(DriveConstants.vel_deadband)
            .with_rotational_deadband(DriveConstants.rot_deadband)
            .with_drive_request_type(  # idk this was in the template code
                phoenix6.swerve.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            )
            .with_velocity_x(x * DriveConstants.max_vel)
            .with_velocity_y(y * DriveConstants.max_vel)
            .with_rotational_rate(z * DriveConstants.max_rot)
        )

    def target(
        self,
        goal: wpimath.geometry.Pose2d,
        facing=wpimath.geometry.Rotation2d(0),
    ):  # the formatter made this really tall
        pose = self.get_state().pose
        x = self.xcontroller.calculate(pose.X(), self.goal_pose.X())
        y = self.ycontroller.calculate(pose.Y(), self.goal_pose.Y())
        r = -self.spinner.calculate(
            wpimath.angleModulus(self.heading_radians()),
            wpimath.angleModulus(self.goal_pose.rotation().radians()),
        )
        self.pid_info = (
            f"X: {pose.X()} -> {self.goal_pose.X()} -> {x}\n"
            f"Y: {pose.Y()} -> {self.goal_pose.Y()} -> {y}\n"
            f"R: {wpimath.angleModulus(self.heading_radians())} -> {wpimath.angleModulus(self.goal_pose.rotation().radians())} -> {r}\n"
        )
        self.go(x, y, r, field_centric=True)

    def brake(self):
        self.request = phoenix6.swerve.requests.SwerveDriveBrake()

    # wpimath.geometry.Rotation2d ?
    def point(self, direction: phoenix6.swerve.Rotation2d):
        self.request = phoenix6.swerve.requests.PointWheelsAt().with_module_direction(
            direction
        )

    def set(self, request: phoenix6.swerve.requests.SwerveRequest):
        self.request = request

    # ran automatically (periodic)
    def execute(self):
        self.set_control(self.request)

    # these values are pushed to NetworkTables

    @feedback
    def speed(self) -> list[float]:
        return list(map(lambda x: x.speed, self.get_state().module_targets))

    @feedback
    def angle(self) -> list[float]:
        return list(map(lambda x: x.angle.degrees(), self.get_state().module_targets))

    @feedback
    def pose(self) -> list[float]:
        pose = self.get_state().pose
        return [pose.X(), pose.Y(), pose.rotation().degrees()]

    @feedback
    def heading(self) -> float:
        return self.gyro.getRotation2d().degrees()

    def heading_radians(self) -> float:
        return self.gyro.getRotation2d().radians()

    @feedback
    def goal(self) -> list[float]:
        return [
            self.goal_pose.X(),
            self.goal_pose.Y(),
            self.goal_pose.rotation().degrees(),
        ]

    @feedback
    def pid(self) -> str:
        return self.pid_info
