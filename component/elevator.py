import phoenix6
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.TalonFX
    elevatorMotor2: phoenix6.hardware.TalonFX
    # encoder: ?

    x = will_reset_to(0)

    # TODO: Adjust PID
    controller = wpimath.controller.PIDController(1, 0, 0)

    def set(self, goal):
        self.x = goal

    def execute(self):
        # elevatorMotor1.set(self.controller.calculate(
        # encoder.pose, self.x
        # ))
