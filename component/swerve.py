import wpilib
import wpimath, wpimath.controller, wpimath.trajectory
import phoenix6

from magicbot import feedback, will_reset_to

from constant import TunerConstants, DriveConstants


class Swerve(phoenix6.swerve.SwerveDrivetrain):

    gyro: phoenix6.hardware.Pigeon2
    request = will_reset_to(
        phoenix6.swerve.requests.Idle()
    )  # default request if no request is given

    # TODO: Adjust PIDs?
    controller = wpimath.controller.HolonomicDriveController(
        wpimath.controller.PIDController(1, 0, 0),
        wpimath.controller.PIDController(1, 0, 0),
        wpimath.controller.ProfiledPIDControllerRadians(
            1, 0, 0, wpimath.trajectory.TrapezoidProfileRadians.Constraints(6.28, 3.14)
        ),
    )

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

        if phoenix6.utils.is_simulation():
            ...

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
        velocity=0.5,
        facing=wpimath.geometry.Rotation2d(0),
    ):  # the formatter made this really tall
        self.go(
            *self.controller.calculate(self.get_state().pose, goal, velocity, facing)
        )

    def brake(self):
        self.request = phoenix6.swerve.requests.SwerveDriveBrake()

    # wpimath.geometry.Rotation2d ?
    def point(self, direction: phoenix6.swerve.Rotation2d):
        self.request = phoenix6.swerve.requests.PointWheelsAt().with_module_direction(
            direction
        )

    def set(self, request: phoenix6.swerve.requests.SwerveRequest):
        self.request = request

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
        return [pose.x, pose.y]

    @feedback
    def heading(self) -> float:
        return self.gyro.getRotation2d().degrees()

    # ran automatically (periodic)
    def execute(self):
        self.set_control(self.request)
