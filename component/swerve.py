import wpilib
import phoenix6

from magicbot import feedback, will_reset_to

from constant import TunerConstants, DriveConstants


class Swerve(phoenix6.swerve.SwerveDrivetrain):

    request = will_reset_to(
        phoenix6.swerve.requests.Idle()
    )  # default request if no request is given

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

    def go(self, x, y, z):  # convenience
        self.request = (
            phoenix6.swerve.requests.FieldCentric()
            .with_deadband(DriveConstants.vel_deadband)
            .with_rotational_deadband(DriveConstants.rot_deadband)
            .with_drive_request_type(  # idk this was in the template code
                phoenix6.swerve.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            )
            .with_velocity_x(x * DriveConstants.max_vel)
            .with_velocity_y(y * DriveConstants.max_vel)
            .with_rotational_rate(z * DriveConstants.max_rot)
        )

    def brake(self):
        self.request = phoenix6.swerve.requests.SwerveDriveBrake()

    def point(self):
        self.request = phoenix6.swerve.requests.PointWheelsAt()

    def set(self, request: phoenix6.swerve.requests.SwerveRequest):
        self.request = request

    # these values are pushed to NetworkTables
    @feedback
    def speed(self) -> list[float]:
        return list(map(lambda x: x.speed, self.get_state().module_targets))

    @feedback
    def angle(self) -> list[float]:
        return list(map(lambda x: x.angle.degrees(), self.get_state().module_targets))

    # ran automatically (periodic)
    def execute(self):
        self.set_control(self.request)
