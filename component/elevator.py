import phoenix6
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.TalonFX
    elevatorMotor2: phoenix6.hardware.TalonFX

    x = will_reset_to(0)

    # TODO: Adjust PID
    controller = wpimath.controller.HolonomicDriveController(
        wpimath.controller.PIDController(1, 0, 0),
        wpimath.controller.PIDController(1, 0, 0),
        wpimath.controller.ProfiledPIDControllerRadians(
            1, 0, 0, wpimath.trajectory.TrapezoidProfileRadians.Constraints(6.28, 3.14)
        ),
    )

    # def move(self, amount):
    #     self.x = amount

    # def execute(self):
    #     motor.set(self.x)

    def target(
        self,
        goal: wpimath.geometry.Pose2d,
        velocity=0.5,
        facing=wpimath.geometry.Rotation2d(0),
    ):  # the formatter made this really tall
        self.go(
            *self.controller.calculate(self.get_state().pose, goal, velocity, facing)
        )

    def execute(self):
        pass
